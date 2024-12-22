import duckdb
import pandas as pd
import datetime
import uuid
from datetime import datetime, timedelta

# Connect to the DuckDB database
con = duckdb.connect('data_facility.db')

# Read the Excel file into a Pandas DataFrame
excel_file = 'usa_data.csv'
df = pd.read_csv(excel_file)

# Create the table from the DataFrame
con.execute("CREATE TABLE IF NOT EXISTS data AS SELECT ticket_id, region, state, site, subject, description, space, equipment, type, CAST(created_on AS DATE) AS created_on, channel, issue_type, problem_category, problem_subcategory, ticket_state, priority, CAST(SUBSTR(closed_time, 1, 10) AS DATE) AS closed_time, maintenance_team, maintenance_type, ticket_action_type, block, sla_status, CAST(sla_end_date AS DATE) AS sla_end_date FROM df")
        

# List all the tables in the database
result = con.execute("SHOW TABLES")
tables = result.fetchall()
print(tables)

# Create the Topics table
con.execute('''
CREATE TABLE Topics (
    Id UUID PRIMARY KEY,
    Created_On TIMESTAMP,
    Name VARCHAR,
    Module VARCHAR,
    Created_By VARCHAR
);
''')

# Create the Initial_Prompts table
con.execute('''
CREATE TABLE Initial_Prompts (
    Id UUID PRIMARY KEY,
    Display_Name VARCHAR,
    Topic_Id UUID REFERENCES Topics(Id)
,
    Icon VARCHAR,
    Sequence INTEGER,
    Prompt TEXT,
    Is_Featured BOOLEAN,
    Created_On TIMESTAMP,
    API_Endpoint VARCHAR
);
''')

# Create the Conversation table
con.execute('''
CREATE TABLE Conversation (
    Id UUID PRIMARY KEY,
    Name VARCHAR,
    Created_By VARCHAR,
    Created_On TIMESTAMP,
    Active BOOLEAN
);
''')

# Create the Conversation_Logs table
con.execute('''
CREATE TABLE Conversation_Logs (
    Id UUID PRIMARY KEY,
    Conversation_Id UUID REFERENCES Conversation(Id)
,
    Input_Prompt TEXT,
    Response TEXT,
    Created_On TIMESTAMP,
    Created_By VARCHAR
);
''')

topic_name = 'Helpdesk'
module = 'helpdesk'
created_by = 'User'
created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Check if the topic already exists, if not, insert it
result = con.execute('SELECT Id FROM Topics WHERE Name = ?', (topic_name,)).fetchone()
if result is None:
    topic_id = str(uuid.uuid4())
    con.execute('''
    INSERT INTO Topics (Id, Created_On, Name, Module, Created_By)
    VALUES (?, ?, ?, ?, ?)
    ''', (topic_id, created_on, topic_name, module, created_by))
else:
    topic_id = result[0]

# Generate a UUID for Initial Prompts
initial_prompt_id = str(uuid.uuid4())
display_name = 'SLA Compliance Analysis'
icon = 'url/image'
sequence = 1
prompt = 'Load the data from the database and give me insights on Helpdesk Data. The insights can be of 3 to 4 points'
is_featured = True
created_on =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
api_endpoint = '/insights'

# Insert a new row into the Initial_Prompts table
con.execute('''
INSERT INTO Initial_Prompts (Id, Display_Name, Topic_Id, Icon, Sequence, Prompt, Is_Featured, Created_On, API_Endpoint)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (initial_prompt_id, display_name, topic_id, icon, sequence, prompt, is_featured, created_on, api_endpoint))

# Verify insertion
result = con.execute('SELECT * FROM Initial_Prompts').fetchall()
print(result)

# Execute the update query using LIKE
update_query = """
UPDATE data
SET maintenance_team = REPLACE(maintenance_team, 'HCL', 'MCloud')
WHERE maintenance_team LIKE '%HCL%';
"""

con.execute(update_query)

# Commit the changes
con.commit()

# Close the connection
con.close()