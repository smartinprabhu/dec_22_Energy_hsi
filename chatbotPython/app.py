import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, Agent
from typing import Dict, Any
import duckdb
from typing import Union, Literal
from datetime import datetime, date
import requests
from dotenv import load_dotenv
load_dotenv()

database=os.getenv('database')

if os.getenv("groq_api_key"):
    llm_config = {
        "config_list": [
            {
                "model": "llama3-70b-8192",
                "api_key": os.getenv("groq_api_key"),
                "base_url": "https://api.groq.com/openai/v1",
            }
        ],
        "cache_seed": None,  # Turns off caching, useful for testing different models
    }

else:
    raise ValueError("AI configuration error: Missing required environment variables.")



app = Flask(__name__)
CORS(app)

@app.route('/aiassist/initial_screen', methods=['GET'])
def initial_screen():
    con = duckdb.connect(database)
    # Get topics
    topics_result = con.execute('SELECT Name FROM Topics LIMIT 5').fetchall()
    topics = [row[0] for row in topics_result]

    # Get featured prompts
    featured_prompts_result = con.execute('''
    SELECT Display_Name, Sequence, Prompt
    FROM Initial_Prompts
    WHERE Is_Featured = TRUE
    ORDER BY Sequence
    LIMIT 5
    ''').fetchall()
    featured_prompts = [{'Display_Name': row[0], 'Sequence': row[1], 'Prompt': row[2]} for row in featured_prompts_result]

    # Get default topic and prompts for 'Helpdesk'
    default_topic_result = con.execute('SELECT Id FROM Topics WHERE Name = ?', ('Helpdesk',)).fetchone()
    if default_topic_result:
        default_topic_id = default_topic_result[0]
        default_topic_prompts_result = con.execute('''
        SELECT Display_Name, Sequence
        FROM Initial_Prompts
        WHERE Topic_Id = ? AND Sequence IN (1, 4)
        ORDER BY Sequence
        ''', (default_topic_id,)).fetchall()
        default_topic = {
            'Topic_Id': default_topic_id,
            'Prompts': [{'Display_Name': row[0], 'Sequence': row[1]} for row in default_topic_prompts_result]
        }
    else:
        default_topic = {}

    # Get history
    history_result = con.execute('''
    SELECT Id, Name
    FROM Conversation WHERE Active = True
    ORDER BY Created_On DESC
    LIMIT 10
    ''').fetchall()
    history = [{'Conversation_Id': row[0], 'Name': row[1]} for row in history_result]

    response = {
        'topics': topics,
        'featured_prompts': featured_prompts,
        'history': history,
        'default_topic': default_topic
    }
    con.close()
    
    return jsonify(response)

@app.route('/aiassist/general_query', methods=['POST'])
def general_query():
    data = request.json
    message = data.get('message')
    conversation_id = data.get('conversation_id')
    created_by = data.get('created_by', 'user')  # Default to 'user' if not provided

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    user_proxy = UserProxyAgent(
        name="User_proxy",
        system_message="You are a helpful assistant.",
        code_execution_config={
            "work_dir": "groupchat",
            "use_docker": False,
        },
        human_input_mode="NEVER",
        default_auto_reply="TERMINATE",
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    )

    # Classification Agent to determine if the question is SQL-related
    classification_agent = AssistantAgent(
    name="ClassificationAgent",
    llm_config=llm_config,
    system_message="""
    You are an AI model designed to classify user queries. 
    Determine whether the user query is related to SQL (database-related) or general conversation.
    If it's an SQL-related question, return "sql-related question:" and continue; 
    if it's general, return "general question:". Include the user input as it is along with the classification tag.

    Ensure that you have given a corrrect tag for the user question by checking the possibilities of sql question based on the columns in the table:ticket_id,region,state,site,subject,description,space,equipment,type,created_on,channel,issue_type,problem_category,problem_subcategory,ticket_state,priority,closed_time,maintenance_team,maintenance_type,ticket_action_type,block,sla_status,sla_end_date.
    • "What is sql?" is general question; note that if the question including word sql are not always needed sql query genration for fetching data. So consider it as a general question.
    """,
    human_input_mode="NEVER",
)

    # Define the Rephraser Agent to rephrase user queries
    rephraser_agent = AssistantAgent(
        name="RephraserAgent",
        llm_config=llm_config,
        system_message="""
        Your role is to enhance the clarity of user queries for natural language processing tasks. Rephrase the user's input into a clear, concise question while maintaining the user's intent. Do not generate SQL queries.

        • If the previous agent's response contains the phrase "general question:", inform the SQL converter not to generate an SQL query in the response, and ensure the JSON response includes: An empty "chart_data" array and "chart_type": "Chart not available" and you must give only the answer to the user's question in the "explanation" node.
        • If the previous agent's response contains the phrase "general question:", ensure you have answered that question in the mentioned format {"chart": { "chart_data": [], "chart_type": "Chart not available"  }, "explanation": "Answer to the question." }. 
        • Even if it is error message, you must ensure to return it in 'explanation' node in the above JSON format.
        • If the previous agent's response includes "sql-related question:", only pass the rephrased question to the next agent.         
        """,
        human_input_mode="NEVER",
    )

    # Define the LLM model for converting natural language to SQL and retrieve data
    sql_converter = AssistantAgent(
        name="SQL_converter",
        llm_config=llm_config,
        system_message="""
        You are an advanced AI model built to only convert natural language queries into SQL queries for retrieving facility management information. The relevant data is stored in a table named data. This table contains the following columns: ticket_id, region, state, site, subject, description, space, equipment, type, created_on, channel, issue_type, problem_category, problem_subcategory, ticket_state, priority, closed_time, maintenance_team, maintenance_type, ticket_action_type, block, sla_status, and sla_end_date.
        Key Column Definitions:
        •   ticket_id: Unique identifier for each ticket.
        •   region: Geographical region where the issue occurred (e.g., South, West).
        •   state: Specific state within the region (e.g., Florida, Texas).
        •   site: Specific location within the state (e.g., Miami South, Austin Downtown).
        •   subject: Brief description or title of the issue.
        •   description: Detailed description of the issue.
        •   space: Specific area within the site where the issue occurred.
        •   equipment: Physical asset or equipment involved in the issue.
        •   type: Category of the ticket (e.g., Asset, Equipment).
        •   created_on: Date the ticket was created.
        •   channel: Communication channel used to report the issue.
        •   issue_type: Type of issue reported (e.g., Request, Incident, Complaint).
        •   problem_category: General category of the problem (e.g., Air Condition, Cleaning).
        •   problem_subcategory: Specific subcategory of the problem.
        •   ticket_state: Current status of the ticket (e.g., Closed, Open).
        •   priority: Priority level assigned to the ticket (e.g., High, Normal).
        •   closed_time: Date and time when the ticket was closed.
        •   maintenance_team: Team responsible for handling the issue.
        •   maintenance_type: Type of maintenance work performed.
        •   ticket_action_type: Action taken on the ticket (e.g., Proactive, Reactive).
        •   block: Specific section within the site.
        •   sla_status: Status of the Service Level Agreement for the ticket (e.g., Within SLA, SLA Elapsed).
        •   sla_end_date: Deadline for the SLA associated with the ticket.

        To handle date formatting and manipulation in DuckDB, follow these guidelines:

        •   Use DATE_TRUNC to truncate dates to the start of a specified period (e.g., year, month).
        •   The function DATE_SUB is not a valid DuckDB function. Instead of DATE_SUB, you should use INTERVAL to subtract time from dates or timestamps.
        •   Use FORMAT_DATE to format dates as strings if needed.
        •   To filter records by the current year, use: DATE_TRUNC('year', created_on) = DATE_TRUNC('year', CURRENT_DATE).
        •   For the current date, use: SELECT CURRENT_DATE;.
        •   To filter records by a specific year (e.g., 2024), use: EXTRACT(YEAR FROM created_on) = 2024.
        •   Ensure DATEDIFF uses the correct syntax: DATEDIFF('DAY', created_on, closed_time).
        •   Replace unsupported functions with DuckDB-compatible ones. For example, use CAST to convert date fields into strings if necessary.
        
        Guidelines:
        •   Ensure the SQL queries map user questions accurately to the corresponding columns based on the provided schema.
        •   Match user inputs to the correct letter casing in the dataset.
        •   Correct spelling errors by mapping common misspellings to standardized values.
        •   Handle date formats by converting them to the YYYY-MM-DD format.
        •   Distinguish between geographical regions (region) and administrative states (state).
        •   Ensure the query reflects user intent while securing against SQL injection and optimizing performance.
        •   Retrieve data from the database, executing the generated SQL query, and return the results clearly without including system details or internal processes.
        •   For ambiguous or unclear queries, prompt the user for clarification to ensure accuracy.
        •   Avoid displaying technical error messages or SQL queries directly in responses.
        •   Handle queries in other languages by translating them if possible or requesting the user to rephrase in English.
        Your primary role is to generate only SQL queries based on user input and present the resulting data in a clear, user-friendly format. Make sure the responses are free from technical details and internal system messages.
        Your response should contain only the SQL query, not any other message or assuming sample values.
        Ensure you don't generate sql query, if previous agent ask you not to generate sql query.
        """,
        
        human_input_mode="NEVER"
    )

     # New SQL Review Agent
    sql_review_agent = AssistantAgent(
        name="SQLReviewAgent",
        llm_config=llm_config,
        system_message="""
        You are an expert in SQL and DuckDB syntax. Your task is to review the generated SQL query by sql_converter agent to ensure it's compatible with DuckDB and matches the correct table columns. 
        Ensure you are returning the sql query in the format of {"Sql_query_gen":";"}.
        If there are any errors, fix them and generate the correct SQL query.
        
        Key points to verify:
        - Correct table and column names based on the schema.
        - Compatibility of SQL functions with DuckDB.
        - Proper handling of data types (e.g., date formats).
        - No syntax errors or invalid references.
        - The function DATE_SUB is not a valid DuckDB function. Ensure you are replacing DATE_SUB with correct function. 
        - Instead of DATE_SUB, you should use INTERVAL to subtract time from dates or timestamps (Example: DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '6 month').

        If errors are found, provide the corrected SQL query, else return same query.
        """,
        human_input_mode="NEVER",
    )

    # Define the new Formatter Agent
    formatter_agent = AssistantAgent(
        name="FormatterAgent",
        llm_config=llm_config,
        system_message="""
You are an expert in formatting and structuring data. Your task is to take the 'results_dict' containing a list of values, identify the type of data as 'single type of values' or 'multiple types of values' and then structure it as valid JSON that can be directly used to create a Plotly chart.
        Provide chart_type as 'Table' for single type of values that is if the 'chart_data' consists of single type values (e.g., a list of objects with only one key-value pair) like [{" ":" "},...,{" ":" "}}].

        ### Ensure the response contains only the following nodes:

        1. "chart": This node should contain four properties:
           - "chart_data": A list formatted from the results_dict data. If the response data is large, truncate to only the top 10 results and "make sure you do not include ellipses/triple-dots or '...', comments like '// truncated to top 10 results' or incomplete items". Ensure that entries are fully formed with no trailing commas.           
           - "chart_type": Recommend the best chart type to visualize the data based on the data in the "chart_data" node. Select the best chart type (Bar chart, Pie chart, Line chart, Histogram, Scatter Plot, or Donut chart) based on data context: use Table for single data points, Bar chart/Pie chart/Histogram/Donut chart for category comparisons, Line chart for sequences, and Scatter plot for 2D correlations.
           - "title": Provide a suitable title for the chart based on the context of the data, ensuring concise axis names.
           - "x_axis_label": Assign an appropriate label for the x-axis (e.g., based on the categories or time-related fields from the data), ensuring concise axis names.
           - "y_axis_label": Assign an appropriate label for the y-axis (e.g., based on the numerical values or frequency counts from the data), ensuring concise axis names.

        2. "explanation": This node should only provide a summary of the values/data present in the "chart_data" node, highlighting key trends or points about the 'chart' and the 'table'.
       
        ### Output Formatting Requirements:
        •   Return only valid JSON output that do not include any 'ellipses' or '...' or placeholders while formatting. If truncating data, provide only the top results without adding incomplete objects or '...'. 
        •   Avoid '...', incomplete objects, or placeholders, especially in 'chart_data'.
        •   All objects should be fully formed with proper syntax, ensuring that the JSON array is complete with opening and closing brackets.
        •   Ensure no system messages, references to queries, code, or unnecessary elements are included. 
        •   It is important that you should not guess or assume or add values that are not in the provided data.
        •   If there are more results to handle, format only the "top 10" results to ensure a quicker response.
        •   If no results or an empty result set is found, or if there is an error in retrieving results, return only an error in the "explanation" node with a message asking the user to modify their question like {"chart": { "chart_data": "Chart not available", "chart_type": "Chart not available"  }, "explanation": "No results found for this question. Please try a different question or rephrase this question." }. 
        •   Ensure chart data is not included in the response when an error occurs and error message is passed from the previous agent.

        Make sure you have followed all the above requirements before returning responses.
         """
        )
    
    
    def custom_speaker_selection(last_speaker: Agent, groupchat: GroupChat) -> Union[Agent, Literal['auto', 'manual', 'random', 'round_robin'], None]:
    # Define the desired flow
        flow = [
            user_proxy,       # Step 1: UserProxyAgent Activation
            classification_agent,
            rephraser_agent,  # Step 2: Rephrase the query
            sql_converter,    # Step 3: Generate and execute SQL
            sql_review_agent, # Step 4: Review and fix the SQL query
            user_proxy,       # Step 5: Interaction for fetching database results
            formatter_agent,  # Step 6: Process results
            user_proxy        # Step 7: Send the response and terminate
        ]
    

    # Check if there are at least two messages in the group chat to avoid out-of-range errors
        if len(groupchat.messages) > 1:
        # Check if the first message indicates a general question
            if 'general question' in groupchat.messages[1]['content'].lower():
            # If we already reached the rephraser, return None to stop the flow after rephrasing
                if last_speaker == rephraser_agent:
                    return None  # Stop the flow entirely after rephraser_agent
                return rephraser_agent  # Move to the rephraser agent and stop progressing further

    
    # Get the current step based on the number of messages
        current_step = len(groupchat.messages) % len(flow)
    
    # Select the next speaker based on the current step
        next_speaker = flow[current_step]
    
    # If we've reached the last step, end the conversation
        if current_step == len(flow) - 1:
            return None  # Terminate the conversation
    
        return next_speaker

    
    
    group_chat = GroupChat(
        agents=[user_proxy,classification_agent, rephraser_agent, sql_converter, sql_review_agent, formatter_agent],
        messages=['You are a helpful assistant skilled at coordinating a group of other assistants to solve a task. '],
        speaker_selection_method=custom_speaker_selection, 
        allow_repeat_speaker=False,   #allow_repeat_speaker=[sql_converter],
    )

    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
        is_termination_msg = lambda x: x.get("content", "").find("TERMINATE") >= 0,
        code_execution_config={
            "last_n_messages": 1,
            "work_dir": "groupchat",
            "use_docker": False,
        },
    )
   
    # Register a function to convert natural language to SQL
    @user_proxy.register_for_execution()
    @sql_review_agent.register_for_llm(description="Review SQL query for correctness and DuckDB compatibility")
    def convert_to_sql(Sql_query_gen: str)-> Dict: #[str, Any]
       
       # Connect to a DuckDB database file
       conn = duckdb.connect(database)
       cur = conn.cursor()

       # Load the CSV file into a pandas DataFrame
       df = pd.read_csv(os.getenv('usa_data_FP'))

       # Convert all data to lowercase
       df = df.apply(lambda x: x.astype(str).str.lower())

       # Insert the DataFrame into a DuckDB table
       conn.execute("CREATE TABLE IF NOT EXISTS data AS SELECT ticket_id, region, state, site, subject, description, space, equipment, type, CAST(created_on AS DATE) AS created_on, channel, issue_type, problem_category, problem_subcategory, ticket_state, priority, CAST(SUBSTR(closed_time, 1, 10) AS DATE) AS closed_time, maintenance_team, maintenance_type, ticket_action_type, block, sla_status, CAST(sla_end_date AS DATE) AS sla_end_date FROM df")
 
    
       try:
        
        #Execute the SQL query
        cur.execute(Sql_query_gen)
            
        #Fetch the results
        rows = cur.fetchall()

        if not rows:
            return {"error": "No results found for the query. Please try a different question or rephrase this question."}


        # Give the results
        # Convert result rows into dictionaries
        result_list = []
        for row in rows:
            row_dict = dict(zip([desc[0] for desc in cur.description], row))

            # Convert any date fields to string format
            for key, value in row_dict.items():
                if isinstance(value, (datetime, pd.Timestamp)):
                    row_dict[key] = value.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
                elif isinstance(value, date):
                    row_dict[key] = value.strftime('%Y-%m-%d')
                elif isinstance(value, (list, dict)):  # Example: Ensure lists and dicts are converted to strings
                    row_dict[key] = str(value)
            result_list.append(row_dict)

       except Exception as e:
        return {"error": "An error occurred while processing your query. Please try again."}
    
  
       finally:
          # Close the connection to the database
          conn.close()

       return {"results": result_list}
    
    try:
        # Process the user query using the sql_converter_agent
        user_proxy.initiate_chat(manager, message=message, clear_history=True)
        # Check the content of the message at index 1
        if 'general question' in group_chat.messages[1]['content'].lower():
            # Return response for general question
            response = group_chat.messages[2]['content']
        elif 'sql-related question' in group_chat.messages[1]['content'].lower():
            # Return response for SQL-related question
            response = group_chat.messages[-1]['content']
        else:
            # Default response if no conditions match
            response = "No specific response found."

    except Exception as e:
        response = "An error occurred while processing your request. Please try again or try asking a different question."


    # Connect to DuckDB and save the conversation log
    con = duckdb.connect(database)  # Adjust the database name/path as needed
    current_time = datetime.now()


    if conversation_id:
        # Check if the conversation_id exists
        existing_conversation = con.execute('SELECT Id FROM Conversation WHERE Id = ?', (conversation_id,)).fetchone()
        
        if existing_conversation:
            # Insert log into existing conversation
            con.execute('''
            INSERT INTO Conversation_Logs (Id, Conversation_Id, Input_Prompt, Response, Created_On, Created_By)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (str(uuid.uuid4()), conversation_id, message, response, current_time, created_by))

            con.close()
            return jsonify({'message': 'Log added to existing conversation', 'conversation_id': conversation_id, 'response': response})
        else:
            return jsonify({'error': 'Conversation ID does not exist'}), 400

    else:
        # Create a new conversation
        new_conversation_id = str(uuid.uuid4())
        con.execute('''
        INSERT INTO Conversation (Id, Name, Created_By, Created_On, Active)
        VALUES (?, ?, ?, ?, ?)
        ''', (new_conversation_id, message, created_by, current_time, True))

        # Insert log into the new conversation
        con.execute('''
        INSERT INTO Conversation_Logs (Id, Conversation_Id, Input_Prompt, Response, Created_On, Created_By)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (str(uuid.uuid4()), new_conversation_id, message, response, current_time, created_by))
        con.close()
        return jsonify({'message': message, 'conversation_id': new_conversation_id, 'response': response})



@app.route('/aiassist/conversation_logs', methods=['POST'])
def conversation_logs():
    data = request.get_json()
    conversation_id = data.get('Id')

    if not conversation_id:
        return jsonify({'error': 'Missing conversation_id parameter'}), 400

    con = duckdb.connect(database)

    # Fetch logs for the given conversation_id
    logs_result = con.execute('''
    SELECT Id, Input_Prompt, Response, Created_On, Created_By
    FROM Conversation_Logs
    WHERE Conversation_Id = ?  
    ORDER BY Created_On
    ''', (conversation_id,)).fetchall()
    
    logs = [{
        'Id': row[0],
        'Input_Prompt': row[1],
        'Response': row[2],
        'Created_On': row[3],
        'Created_By': row[4]
    } for row in logs_result]
    con.close()
    return jsonify({'conversation_logs': logs})


@app.route('/aiassist/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get("message")
    conversation_id = data.get('conversation_id')
    created_by = data.get('created_by', 'user')  # Default to 'user' if not provided

    if not message:
        return jsonify({'error': 'Message is required'}), 400
   
    user_proxy = UserProxyAgent(
        name="User_proxy",
        system_message="You are a helpful assistant.",
        code_execution_config={
            "work_dir": "groupchat",
            "use_docker": False,
        },
        human_input_mode="NEVER",
        default_auto_reply="TERMINATE",
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    )

    sla_assistant = AssistantAgent(
        name="SLA_assistant",
        llm_config=llm_config,
        system_message = """
        You are tasked with performing an in-depth analysis on the sla_status from the provided helpdesk data related to facility management. 
        Your objective is give code to generate actionable insights by understanding each column through Exploratory Data Analysis (EDA) and also answer the question asked by the user correctly. 
        Begin by loading the provided dataset and conducting EDA to understand the unique values in each column. 
        If a specific time frame is mentioned such as last week or last month or a specfic month, filter the data and then calculate the overall SLA compliance rate and identify why it is not 100%, 
        focusing specifically on the non-compliance instances where sla_status is SLA Elapsed. Use the column created_on. If the data returned by the function is NaN for specific time frame, return that there is no enough data.
        Identify and extract relevant factors such as problem_category, problem_subcategory, maintenance_team, site and region that impact SLA compliance. 
        Determine if the SLA Elapsed status is influenced by the unique values in problem_category, problem_subcategory, site ,region and maintenance_team. 
        Identify the top maintenance_team with the highest number of SLA Elapsed cases and specify the problem_category or site or region most frequently associated with these teams.
        Analyze the data entries that did not meet SLA requirements to identify common reasons for non-compliance and provide actionable insights to improve SLA compliance.
        keep it simple. Dont make the insights look too wordy. Dont execute with dummy data. If you are not able to answer the question, reply you are not able to.
        If no data is returned by the function, return that you dont have enough data. your final answer should be a accurately answer the question and never include messages about the function in the prompt.
        There should be nothing like these '<tool-use>{"tool_calls"}</tool-use>' when printing the insights.
        dont return something like this Please call the following tool: {"function":{"name":"analyze"},"parameters":{"time_period":"2023-08-01 to 2023-08-31"}}
        """,
        human_input_mode="NEVER",
    )

    group_chat = GroupChat(
        agents=[user_proxy, sla_assistant],
        messages=['You are a helpful assistant skilled at coordinating a group of other assistants to solve a task.'],
        speaker_selection_method='auto',
        allow_repeat_speaker=False
    )

    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
        is_termination_msg = lambda x: x.get("content", "").find("TERMINATE") >= 0,
        code_execution_config={
            "last_n_messages": 1,
            "work_dir": "groupchat",
            "use_docker": False,
        },
    )

    @user_proxy.register_for_execution()
    @sla_assistant.register_for_llm(description="SLA compliance analyzer with time frame")
    def analyze() -> Dict[str, Any]:
        # Connect to DuckDB and fetch data
        conn = duckdb.connect(database)
        data = conn.execute("SELECT * FROM data")
        df = data.fetch_df()
        filtered_df = df

        # Debug: Print the shape of the filtered data
        print(f"Filtered data shape: {filtered_df.shape}")

        # Filter data for SLA Elapsed
        sla_elapsed_df = filtered_df[filtered_df['sla_status'] == 'SLA Elapsed']

        # Calculate overall SLA compliance rate
        sla_compliance_rate = round((filtered_df['sla_status'] != 'SLA Elapsed').mean() * 100, 2)

        # Identify and extract relevant factors impacting SLA compliance
        relevant_factors = ['problem_category', 'problem_subcategory', 'maintenance_team']
        analysis_results = {
            'sla_compliance_rate': sla_compliance_rate,
            'top_10_factors': {},
            'maintenance_team_problem_categories': {},
            'site_sla_elapsed_counts': {},
            'region_sla_elapsed_counts': {},
            'maintenance_team_site_region_counts': {}
        }

        for factor in relevant_factors:
            # Calculate SLA Elapsed instances grouped by factor
            sla_elapsed_counts = sla_elapsed_df.groupby(factor).size().sort_values(ascending=False)

            # Display only the top 10 entries
            top_10 = sla_elapsed_counts.head(10)
            analysis_results['top_10_factors'][factor] = top_10.to_dict()

            # For maintenance_team, also show which problem categories have SLA Elapsed
            if factor == 'maintenance_team':
                analysis_results['maintenance_team_problem_categories'] = {}
                for team in top_10.index:
                    team_df = sla_elapsed_df[sla_elapsed_df['maintenance_team'] == team]
                    problem_categories = team_df['problem_category'].value_counts().sort_values(ascending=False)
                    analysis_results['maintenance_team_problem_categories'][team] = problem_categories.to_dict()

        # Calculate SLA non-compliance counts by site
        site_sla_elapsed_counts = sla_elapsed_df['site'].value_counts().sort_values(ascending=False)
        analysis_results['site_sla_elapsed_counts'] = site_sla_elapsed_counts.to_dict()

        # Calculate SLA non-compliance counts by region
        region_sla_elapsed_counts = sla_elapsed_df['region'].value_counts().sort_values(ascending=False)
        analysis_results['region_sla_elapsed_counts'] = region_sla_elapsed_counts.to_dict()

        # Calculate maintenance team SLA non-compliance counts by site and region
        maintenance_team_site_region_counts = sla_elapsed_df.groupby(['maintenance_team', 'site', 'region']).size().sort_values(ascending=False)
        maintenance_team_site_region_counts_dict = {}
        for (team, site, region), count in maintenance_team_site_region_counts.items():
            if team not in maintenance_team_site_region_counts_dict:
                maintenance_team_site_region_counts_dict[team] = {}
            if site not in maintenance_team_site_region_counts_dict[team]:
                maintenance_team_site_region_counts_dict[team][site] = {}
            maintenance_team_site_region_counts_dict[team][site][region] = count
        analysis_results['maintenance_team_site_region_counts'] = maintenance_team_site_region_counts_dict

        conn.close()
        return analysis_results


    user_proxy.initiate_chat(manager, message=message, clear_history=True)
    response = group_chat.messages[-2]['content']
    # Connect to DuckDB and save the conversation log
    con = duckdb.connect(database)
    current_time = datetime.now()

    if conversation_id:
        # Check if the conversation_id exists
        existing_conversation = con.execute('SELECT Id FROM Conversation WHERE Id = ?', (conversation_id,)).fetchone()
        
        if existing_conversation:
            # Insert log into existing conversation
            con.execute('''
            INSERT INTO Conversation_Logs (Id, Conversation_Id, Input_Prompt, Response, Created_On, Created_By)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (str(uuid.uuid4()), conversation_id, message, response, current_time, created_by))

            con.close()
            return jsonify({'message': 'Log added to existing conversation', 'conversation_id': conversation_id})
        else:
            return jsonify({'error': 'Conversation ID does not exist'}), 400

    else:
        # Create a new conversation
        new_conversation_id = str(uuid.uuid4())
        con.execute('''
        INSERT INTO Conversation (Id, Name, Created_By, Created_On, Active)
        VALUES (?, ?, ?, ?, ?)
        ''', (new_conversation_id, message, created_by, current_time, True))

        # Insert log into the new conversation
        con.execute('''
        INSERT INTO Conversation_Logs (Id, Conversation_Id, Input_Prompt, Response, Created_On, Created_By)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (str(uuid.uuid4()), new_conversation_id, message, response, current_time, created_by))
        con.close()
        return jsonify({'message': message ,'conversation_id': new_conversation_id, 'response': response})


@app.route('/aiassist/insights', methods=['POST'])
def insights():
    # Predefined message
    message = 'Load the data from the database and conduct EDA and give me insights on SLA compliance and the problem_category and maintenance_team affecting the SLA compliance. Also Give me some insights to Analyze the SLA compliance for sites and the corresponding maintenance team working in that site and region. The insights can be of 6 to 7 points'
    
    user_proxy = UserProxyAgent(
        name="User_proxy",
        system_message="You are a helpful assistant.",
        code_execution_config={
            "work_dir": "groupchat",
            "use_docker": False,
        },
        human_input_mode="NEVER",
        default_auto_reply="TERMINATE",
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    )

    sla_assistant = AssistantAgent(
        name="SLA_assistant",
        llm_config=llm_config,
        system_message = """
        You are tasked with performing an in-depth analysis on the sla_status from the provided helpdesk data related to facility management. 
        Your objective is give code to generate actionable insights by understanding each column through Exploratory Data Analysis (EDA) and also answer the question asked by the user correctly. 
        Begin by loading the provided dataset and conducting EDA to understand the unique values in each column. 
        If a specific time frame is mentioned such as last week or last month or a specfic month, filter the data and then calculate the overall SLA compliance rate and identify why it is not 100%, 
        focusing specifically on the non-compliance instances where sla_status is SLA Elapsed. Use the column created_on. If the data returned by the function is NaN for specific time frame, return that there is no enough data.
        If Time period is not mentioned then use the entire data.
        Identify and extract relevant factors such as problem_category, problem_subcategory, and maintenance_team that impact SLA compliance. 
        Determine if the SLA Elapsed status is influenced by the unique values in problem_category, problem_subcategory, and maintenance_team. 
        Identify the top maintenance_team with the highest number of SLA Elapsed cases and specify the problem_category most frequently associated with these teams.
        Analyze the data entries that did not meet SLA requirements to identify common reasons for non-compliance and provide actionable insights to improve SLA compliance.
        If the time period for the function is in words, convert it to date format YYYY-MM-DD. Example: March 12 2023 : 2023-03-12 or if it is 'march 12 2023 to august 12 2023' then it should be '2023-03-12 to 2023-08-12'.
        keep it simple. Dont make the insights look too wordy. Dont execute with dummy data. If you are not able to answer the question, reply you are not able to.
        If no data is returned by the function, return that you dont have enough data. your final answer should be a summary of the insights and never include messages about the function in the prompt.
        There should be nothing like these '<tool-use>{"tool_calls"}</tool-use>' when printing the insights.
        dont return something like this Please call the following tool: {"function":{"name":"analyze"},"parameters":{"time_period":"2023-08-01 to 2023-08-31"}}
        """,
        human_input_mode="NEVER",
    )

    group_chat = GroupChat(
        agents=[user_proxy, sla_assistant],
        messages=['You are a helpful assistant skilled at coordinating a group of other assistants to solve a task.'],
        speaker_selection_method='auto',
        allow_repeat_speaker=False
    )

    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
        is_termination_msg = lambda x: x.get("content", "").find("TERMINATE") >= 0,
        code_execution_config={
            "last_n_messages": 1,
            "work_dir": "groupchat",
            "use_docker": False,
        },
    )

    @user_proxy.register_for_execution()
    @sla_assistant.register_for_llm(description="SLA compliance analyzer with time frame")
    def analyze() -> Dict[str, Any]:
        # Connect to DuckDB and fetch data
        conn = duckdb.connect(database)
        data = conn.execute("SELECT * FROM data")
        df = data.fetch_df()
        
        # Ensure the 'created_on' column is parsed as datetime
        df["created_on"] = pd.to_datetime(df["created_on"], errors='coerce')

        filtered_df = df

        # Debug: Print the shape of the filtered data
        print(f"Filtered data shape: {filtered_df.shape}")

        # Filter data for SLA Elapsed
        sla_elapsed_df = filtered_df[filtered_df['sla_status'] == 'SLA Elapsed']

        # Calculate overall SLA compliance rate
        sla_compliance_rate = round((filtered_df['sla_status'] != 'SLA Elapsed').mean() * 100, 2)

        # Identify and extract relevant factors impacting SLA compliance
        relevant_factors = ['problem_category', 'problem_subcategory', 'maintenance_team']
        analysis_results = {
            'sla_compliance_rate': sla_compliance_rate,
            'top_10_factors': {},
            'maintenance_team_problem_categories': {},
            'site_sla_elapsed_counts': {},
            'region_sla_elapsed_counts': {},
            'maintenance_team_site_region_counts': {}
        }

        for factor in relevant_factors:
            # Calculate SLA Elapsed instances grouped by factor
            sla_elapsed_counts = sla_elapsed_df.groupby(factor).size().sort_values(ascending=False)

            # Display only the top 10 entries
            top_10 = sla_elapsed_counts.head(10)
            analysis_results['top_10_factors'][factor] = top_10.to_dict()

            # For maintenance_team, also show which problem categories have SLA Elapsed
            if factor == 'maintenance_team':
                analysis_results['maintenance_team_problem_categories'] = {}
                for team in top_10.index:
                    team_df = sla_elapsed_df[sla_elapsed_df['maintenance_team'] == team]
                    problem_categories = team_df['problem_category'].value_counts().sort_values(ascending=False)
                    analysis_results['maintenance_team_problem_categories'][team] = problem_categories.to_dict()

        # Calculate SLA non-compliance counts by site
        site_sla_elapsed_counts = sla_elapsed_df['site'].value_counts().sort_values(ascending=False)
        analysis_results['site_sla_elapsed_counts'] = site_sla_elapsed_counts.to_dict()

        # Calculate SLA non-compliance counts by region
        region_sla_elapsed_counts = sla_elapsed_df['region'].value_counts().sort_values(ascending=False)
        analysis_results['region_sla_elapsed_counts'] = region_sla_elapsed_counts.to_dict()

        # Calculate maintenance team SLA non-compliance counts by site and region
        maintenance_team_site_region_counts = sla_elapsed_df.groupby(['maintenance_team', 'site', 'region']).size().sort_values(ascending=False)
        maintenance_team_site_region_counts_dict = {}
        for (team, site, region), count in maintenance_team_site_region_counts.items():
            if team not in maintenance_team_site_region_counts_dict:
                maintenance_team_site_region_counts_dict[team] = {}
            if site not in maintenance_team_site_region_counts_dict[team]:
                maintenance_team_site_region_counts_dict[team][site] = {}
            maintenance_team_site_region_counts_dict[team][site][region] = count
        analysis_results['maintenance_team_site_region_counts'] = maintenance_team_site_region_counts_dict

        conn.close()
        return analysis_results
    user_proxy.initiate_chat(manager, message=message, clear_history=True)
    response = group_chat.messages[-2]['content']
    return jsonify({'insights': response})

    
@app.route('/aiassist/delete_all', methods=['DELETE'])
def delete_all_rows():
    try:
        conn = duckdb.connect(database)
        conn.execute("UPDATE Conversation SET Active = FALSE")
        conn.close()
        return jsonify({"message": "All rows deleted from ConversationLogs"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(port=5001, debug=True)
