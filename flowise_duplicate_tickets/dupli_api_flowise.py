from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Base URL of the other Flask API (used to get ticket details and check for duplicates)
base_url = os.getenv("BASE_URL")


app = Flask(__name__)

def fetch_ticket_details(ticket_id):
    """Fetch ticket details from the API."""
    try:
        response = requests.get(f"{base_url}/get_ticket/{ticket_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch ticket details: {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching ticket details: {e}"}

def check_duplicates(ticket_details):
    """Check for duplicate tickets using the API."""
    payload = {
        "Ticket ID": ticket_details['ticket_id'],
        "Subject": ticket_details['subject'],
        "Problem Category": ticket_details['problem_category'],
        "Problem Sub Category": ticket_details['problem_sub_category'],
        "Type": ticket_details['type'],
        "Space": ticket_details['space'],
        "Equipment": ticket_details['equipment'],
        "Description": ticket_details['description'],
        "Created On": ticket_details['created_on'],
        "Company_name": ticket_details['company_name'],
        "Region": ticket_details['region']
    }

    try:
        duplicate_response = requests.post(f"{base_url}/find_duplicates", json=payload)
        if duplicate_response.status_code == 200:
            return duplicate_response.json()
        else:
            return {"error": f"Error checking duplicates: {duplicate_response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error checking duplicates: {e}"}

@app.route('/process_ticket/<ticket_id>', methods=['GET'])
def process_ticket(ticket_id):
    # Step 1: Fetch ticket details from the API
    ticket_details = fetch_ticket_details(ticket_id)
    
    if "error" in ticket_details:
        return jsonify(ticket_details), 500

    # Step 2: Check for duplicate tickets
    duplicate_data = check_duplicates(ticket_details)

    if "error" in duplicate_data:
        return jsonify(duplicate_data), 500

    # Prepare final response
    result = {
        "ticket_details": ticket_details,
        "duplicate_check_result": duplicate_data,
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
