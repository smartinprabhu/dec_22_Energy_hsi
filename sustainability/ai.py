from flask import Flask, request, jsonify
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import requests
import logging

from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

database = os.getenv('database')

# Configure logging
logging.basicConfig(level=logging.INFO)

# LLM configuration
llm_config = {
    "config_list": [
        {
            "model": "llama3-70b-8192",
            "api_key": os.getenv('groq_api_key'),  # This will fetch the API key from the .env file
            "base_url": "https://api.groq.com/openai/v1"
        }
    ],
    "cache_seed": None  # Turns off caching, useful for testing different models
}

app = Flask(__name__)
CORS(app)

# Define API endpoints
data_api_url = 'http://127.0.0.1:5003/forecast'

# Fetch data from the API
def fetch_data():
    try:
        logging.info(f"Fetching data from {data_api_url}")
        response = requests.post(data_api_url)
        response.raise_for_status()
        logging.info(f"Successfully fetched data from {data_api_url}")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return None

def extract_necessary_data(plot_data):
    necessary_data = {}
    if isinstance(plot_data, dict):
        for key, value in plot_data.items():
            if isinstance(value, dict) and 'data' in value:
                necessary_data[key] = value['data']
            elif isinstance(value, list):
                necessary_data[key] = value
    elif isinstance(plot_data, list):
        necessary_data = plot_data
    return necessary_data

def create_chart_explainer():
    return AssistantAgent(
        name="chart_explainer",
        system_message="""
        You are an advanced AI model specialized in analyzing various types of charts. You will receive chart data and will need to generate insights, recommendations, use cases based on the chart. Do not summarize the data or highlight specific data points. Focus on the significance, implications, and potential actions or improvements suggested by the chart. Ensure that your responses are clear, accurate, and tailored to the specific type of chart provided, whether it's a pie chart, bar chart, line chart, or any other type.
        """,
        llm_config=llm_config,
        human_input_mode="NEVER"
    )

# Define the User Proxy Agent
def create_user_proxy():
    return UserProxyAgent(
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

# Create a GroupChat and GroupChatManager
def create_group_chat():
    chart_explainer = create_chart_explainer()
    user_proxy = create_user_proxy()
    group_chat = GroupChat(
        agents=[user_proxy, chart_explainer],
        messages=['You are a helpful assistant skilled at interpreting the results of various types of charts and deliver only insights, suggestions, improvements, recommendations based on given data (never explain the data).'],
        speaker_selection_method='auto',
        allow_repeat_speaker=False
    )
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
        is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
        code_execution_config={
            "last_n_messages": 1,
            "work_dir": "groupchat",
            "use_docker": False,
        },
    )
    return group_chat, manager

@app.route('/explain_chart', methods=['GET'])
def explain_chart():
    period = request.args.get('period')
    chart_type = request.args.get('chart_type')

    if not period or not chart_type:
        return jsonify({'error': 'Period and chart_type are required'}), 400

    logging.info(f"Processing period: {period}, chart_type: {chart_type}")

    # Fetch data from the API
    fetched_data = fetch_data()
    if fetched_data is None:
        return jsonify({'error': 'Failed to fetch data'}), 500

    logging.info(f"Fetched data: {fetched_data}")

    # Find the specific chart data for the given period and chart type
    chart_data = next((item[1].get(chart_type) for item in fetched_data if item[0] == period), {})

    if not chart_data:
        return jsonify({'error': f'No data found for period: {period}, chart_type: {chart_type}'}), 404

    logging.info(f"Chart data: {chart_data}")

    # Extract necessary data from the Plotly JSON
    necessary_chart_data = extract_necessary_data(chart_data)

    # Create group chat and manager
    group_chat, manager = create_group_chat()
    user_proxy = group_chat.agents[0]

    message_content = f"chart_type: {chart_type}, chart_data: {necessary_chart_data}"

    if chart_type in ['trend_plot', 'utility_plot', 'pie_chart', 'prediction_plot', 'eb_tco2_plot', 'dg_tco2_plot', 'solar_tco2_plot']:
        if chart_type == 'trend_plot':
            # Energy Consumption Trend Analysis
            message_content += "\n\n### Insights and Recommendations\n\n"
            message_content += "- **Dynamic Consumption:** Fluctuations indicate potential inefficiencies or operational changes. Focus on stabilizing these variations.\n"
            message_content += "Recommendation: Implement proactive measures based on trend analysis to optimize energy usage.\n"

        elif chart_type == 'utility_plot':
            # Utility Plot Analysis
            message_content += "\n\n### Insights and Recommendations\n\n"
            message_content += "- **High Consumption Areas:** HVAC and Compressors might need efficiency improvements.\n"
            message_content += "- **Energy Loss:** Reduce the gap between total and utility consumption by addressing inefficiencies.\n"
            message_content += "Recommendation: Optimize energy distribution across utilities and monitor for discrepancies.\n"

        elif chart_type == 'pie_chart':
            # Pie Chart Analysis
            message_content += "\n\n### Insights and Recommendations\n\n"
            message_content += "- **Source Optimization:** Increase Solar usage; it has the highest efficiency.\n"
            message_content += "- **EB Dependency:** Reduce reliance on EB by enhancing alternative sources.\n"
            message_content += "Recommendation: Focus on Solar expansion and optimizing EB usage.\n"

        elif chart_type == 'prediction_plot':
            # Prediction Plot Analysis
            message_content += "\n\n### Insights and Recommendations\n\n"
            message_content += "- **Consumption Patterns:** Yesterday's lower consumption may indicate opportunities to save energy today.\n"
            message_content += "Recommendation: Leverage these patterns to plan for energy efficiency improvements.\n"

        elif chart_type == 'eb_tco2_plot':
            # EB TCO2 Plot Analysis
            message_content += "\n\n### Insights and Recommendations\n\n"
            message_content += "- **CO2 Impact:** Forecasted emissions suggest a need for reduction strategies.\n"
            message_content += "Recommendation: Shift towards renewable energy to lower emissions.\n"

        elif chart_type == 'dg_tco2_plot':
            # DG TCO2 Plot Analysis
            message_content += "\n\n### Insights and Recommendations\n\n"
            message_content += "- **High DG Emissions:** Consider reducing DG usage to lower CO2 emissions.\n"
            message_content += "Recommendation: Explore alternatives to diesel generators.\n"

        elif chart_type == 'solar_tco2_plot':
            # Solar TCO2 Plot Analysis
            message_content += "\n\n### Insights and Recommendations\n\n"
            message_content += "- **Green Energy Progress:** Continue investing in solar projects to meet targets.\n"
            message_content += "Recommendation: Prioritize solar energy expansion for sustainability goals.\n"

    elif chart_type in ['EUI', 'EIO']:
        building_area = 100000  # in square feet
        occupancy = 5000  # per day

        if chart_type == 'EUI':
            message_content += "\n- Explain the concept of Energy Use Intensity (EUI).\n"
            message_content += "- Discuss its significance and implications in energy management.\n"
            message_content += "- Provide insights and recommendations based on the EUI value.\n"
            message_content += f"- Consider the building area of {building_area} square feet and daily occupancy of {occupancy} people.\n"

        elif chart_type == 'EIO':
            message_content += "\n- Explain the concept of Energy Intensity per Capita (EIO).\n"
            message_content += "- Discuss its significance and implications in energy management.\n"
            message_content += "- Provide insights and recommendations based on the EIO value.\n"
            message_content += f"- Consider the building area of {building_area} square feet and daily occupancy of {occupancy} people.\n"

    # Initiate chat with the manager
    user_proxy.initiate_chat(manager, message={"content": message_content}, clear_history=True)

    # Check if the response is generated correctly
    if len(group_chat.messages) < 2:
        logging.error(f"No response generated for chart type: {chart_type}")
        return jsonify({'error': 'No response generated'}), 500

    # Get the explanation response
    response = group_chat.messages[-2]['content']
    logging.info(f"Generated explanation for chart type {chart_type}: {response}")

    return jsonify({'explanation': response})

if __name__ == '__main__':
    app.run(port=5004, debug=True)