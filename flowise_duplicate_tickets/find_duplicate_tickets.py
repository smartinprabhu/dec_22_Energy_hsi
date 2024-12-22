from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import pool
from sklearn.metrics.pairwise import cosine_similarity
from psycopg2.extras import DictCursor
import numpy as np
import gensim
import os
from datetime import datetime
from flask_cors import CORS
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(1, 20, dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'))


# Load Word2Vec model globally once
MODEL_FILE = 'word2vec_model.pkl'
word2vec_model = gensim.models.Word2Vec.load(MODEL_FILE) if os.path.exists(MODEL_FILE) else None

# Vectorize sentence
def vectorize_sentence(model, subject, problem_category, problem_sub_category, type, space, equipment, description):
    sentence = f"{subject} {problem_category} {problem_sub_category} {type} {space} {equipment} {description}"
    words = sentence.split()
    word_vectors = [model.wv[word] for word in words if word in model.wv]
    return np.mean(word_vectors, axis=0) if word_vectors else np.zeros(model.vector_size)

# Find duplicate tickets using Pgvector
def find_duplicate_tickets_pgvector(input_ticket, model, current_time, threshold=0.5):
    input_vector = vectorize_sentence(model, input_ticket['Subject'], input_ticket['Problem Category'], 
                                      input_ticket['Problem Sub Category'], input_ticket['Type'], 
                                      input_ticket['Space'], input_ticket['Equipment'], input_ticket['Description'])

    logger.info("Input Ticket Vector: %s", input_vector)

    conn = connection_pool.getconn()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """
        SELECT ticket_id, company_name, problem_category, problem_sub_category, channel, closed_date, created_on, 
               subject, description, type, space, equipment, issue_type, maintenance_team, priority, status, 
               sla_status, ticket_type, region, actual_duration, ticket_vector <=> %s::vector AS similarity
        FROM hx_helpdesktickets_fordupli
        WHERE status != 'Closed' AND created_on < %s
        ORDER BY similarity ASC
        LIMIT 5;
        """
        cur.execute(query, (input_vector.tolist(), current_time))
        results = cur.fetchall()
    except Exception as e:
        logger.error("Error fetching duplicates: %s", e)
        results = []
    finally:
        cur.close()
        connection_pool.putconn(conn)

    logger.info("Fetched results: %s", results)

    duplicates = [result for result in results if result['similarity'] <= threshold]
    return duplicates


# Helper function to convert date columns and append "IST"
def format_dates_with_ist(ticket_details):
    if 'created_on' in ticket_details:
        ticket_details['created_on'] = f"{ticket_details['created_on']} IST"
    if 'closed_date' in ticket_details:
        ticket_details['closed_date'] = f"{ticket_details['closed_date']} IST"
    # You can add more date fields as needed
    return ticket_details

@app.route('/get_ticket/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    conn = connection_pool.getconn()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Use LOWER() to perform a case-insensitive comparison
        query = "SELECT * FROM hx_helpdesktickets_fordupli WHERE LOWER(ticket_id) = LOWER(%s);"

        cur.execute(query, (ticket_id,))
        ticket_details = cur.fetchone()

        if not ticket_details:
            return jsonify({"message": "Ticket not found."}), 404
        
        # Convert ticket details to a dictionary
        ticket_details_dict = dict(ticket_details)

        # Remove the 'ticket_vector' column if it exists in the dictionary
        ticket_details_dict.pop('ticket_vector', None)
         # Format date fields
        ticket_details_dict = format_dates_with_ist(ticket_details_dict)

        return jsonify(ticket_details_dict)

    except Exception as e:
        logger.error("Error fetching ticket details: %s", e)
        return jsonify({"message": "Error fetching ticket details."}), 500
    finally:
        cur.close()
        connection_pool.putconn(conn)

# Convert the "Mon, 17 Jun 2024 00:00:00 GMT" format to "YYYY-MM-DD HH:MM:SS"
def convert_to_required_format(date_str):
    try:
        # Parse the input date string into a datetime object
        parsed_date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        # Return the datetime in the required "YYYY-MM-DD HH:MM:SS" format
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None  # Return None if parsing fails

@app.route('/find_duplicates', methods=['POST'])
def find_duplicates():
    input_ticket = request.json

    # Get the current time for comparison
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Validate the incoming ticket
    required_keys = ['Ticket ID','Company_name', 'Subject', 'Problem Category', 'Problem Sub Category', 'Type', 'Space', 'Equipment', 'Description','Region']
    if not all(key in input_ticket for key in required_keys):
        return jsonify({"message": "Invalid input. Please provide all required fields."}), 400

    # Fetch input ticket details from the database
    conn = connection_pool.getconn()
    input_ticket_details = None
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM hx_helpdesktickets_fordupli WHERE ticket_id = %s;"
        cur.execute(query, (input_ticket['Ticket ID'],))
        input_ticket_details = cur.fetchone()
    except Exception as e:
        logger.error("Error fetching input ticket details: %s", e)
    finally:
        cur.close()
        connection_pool.putconn(conn)

    if not input_ticket_details:
        return jsonify({"message": "Input ticket not found in the database."}), 404
    
    # Find duplicates using the current time instead of the input ticket's Created On value
    duplicates = find_duplicate_tickets_pgvector(input_ticket, word2vec_model, current_time)

    # Filter out the input ticket ID and mismatched company names from duplicates
    duplicates = [result for result in duplicates if result['ticket_id'] != input_ticket['Ticket ID'] and result['company_name'] == input_ticket['Company_name'] and result['region'] == input_ticket['Region'] ]

    if not duplicates:
        return jsonify({
            "input_ticket": {key: value for key, value in input_ticket_details.items()},
            "confidence_score": 0.0,
            "duplicate_count": 0,
            "duplicate_tickets": [],
            "message": "No duplicate tickets found. You can proceed with solving this ticket."
        })

    confidence_scores = []
    duplicate_tickets = []

    for row in duplicates:


        # Format the date columns with " IST"
        row['closed_date'] = f"{row['closed_date']} IST" if row['closed_date'] else None
        row['created_on'] = f"{row['created_on']} IST" if row['created_on'] else None

        row_problem_category = row.get('problem_category')
        row_problem_sub_category = row.get('problem_sub_category')
        row_space = row.get('space')
        row_equipment = row.get('equipment')
        row_type = row.get('type')
        row_description = row.get('description')

        if (row_problem_category == input_ticket.get('Problem Category') and
            row_problem_sub_category == input_ticket.get('Problem Sub Category') and
            row_space == input_ticket.get('Space') and
            row_equipment == input_ticket.get('Equipment') and
            row_type == input_ticket.get('Type')):

            vector = vectorize_sentence(word2vec_model, input_ticket['Subject'],
                                         input_ticket['Problem Category'],
                                         input_ticket['Problem Sub Category'],
                                         input_ticket['Type'],
                                         input_ticket['Space'],
                                         input_ticket['Equipment'],
                                         input_ticket['Description'])
            row_vector = vectorize_sentence(word2vec_model, row['subject'],
                                             row_problem_category,
                                             row_problem_sub_category,
                                             row_type,
                                             row_space,
                                             row_equipment,
                                             row_description)
            score = cosine_similarity([vector], [row_vector])[0][0]
            confidence_scores.append(score)

            duplicate_ticket_info = {
                key: value for key, value in row.items() if key != 'vector'
            }

            duplicate_ticket_info["Confidence Score"] = float(score)
            duplicate_tickets.append(duplicate_ticket_info)

    confidence_score = float(np.mean(confidence_scores)) if confidence_scores else 0.0
    duplicate_count = len(duplicate_tickets)

    return jsonify({
        #"input_ticket": {key: value for key, value in input_ticket_details.items()},
        "duplicate_count": duplicate_count,
        "duplicate_tickets": duplicate_tickets,
        "message": "Duplicate tickets found. Please check the details before proceeding."
    })


if __name__ == "__main__":
    app.run(debug=True)
