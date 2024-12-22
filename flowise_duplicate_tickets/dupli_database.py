import pandas as pd
import psycopg2
from datetime import datetime
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os
load_dotenv()

# PostgreSQL connection details
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
}

CSV_FILES = ['Helpdesk_new.csv', 'dupli_tickets.csv']

# Load and preprocess data
def load_data(files):
    # Read and concatenate data from multiple CSV files
    dataframes = [pd.read_csv(file) for file in files]
    combined_data = pd.concat(dataframes, ignore_index=True)
    return combined_data

def preprocess_data(data):
    # Convert dots to colons in the time portion of the date
    data['Created On'] = data['Created On'].str.replace('.', ':', regex=False)
    data['Closed Date'] = data['Closed Date'].str.replace('.', ':', regex=False)

    # Convert to datetime, handling multiple formats
    data['Created On'] = pd.to_datetime(data['Created On'], errors='coerce')
    data['Closed Date'] = pd.to_datetime(data['Closed Date'], errors='coerce')

    # Fill NaT with None for compatibility with PostgreSQL
    data['Closed Date'] = data['Closed Date'].where(data['Closed Date'].notna(), None)
    data['Created On'] = data['Created On'].where(data['Created On'].notna(), None)

    # Convert empty strings to None for numeric columns
    data['Actual Duration'] = pd.to_numeric(data['Actual Duration'], errors='coerce')  # Convert to numeric and set invalid parsing to NaN
    data['Actual Duration'] = data['Actual Duration'].fillna(0.0)  # Fill NaN with 0.0

    data = data.fillna('')  # Fill NaN with empty string for other columns
    return data

# Create helpdesk_tickets table without the vector column
def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hx_helpdesktickets_fordupli(
        ticket_id VARCHAR PRIMARY KEY,
        company_name VARCHAR,
        problem_category VARCHAR,
        problem_sub_category VARCHAR,
        channel VARCHAR,
        closed_date TIMESTAMP,
        created_on TIMESTAMP,
        subject VARCHAR,
        description TEXT,
        type VARCHAR,
        space VARCHAR,
        equipment VARCHAR,
        issue_type VARCHAR,
        maintenance_team VARCHAR,
        priority VARCHAR,
        status VARCHAR,
        sla_status VARCHAR,
        ticket_type VARCHAR,
        region VARCHAR,
        actual_duration FLOAT
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Insert new tickets without vectors into PostgreSQL
def insert_new_ticket(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for _, row in data.iterrows():
        closed_date = row['Closed Date']
        created_on = row['Created On']

        # Handle datetime conversion
        if pd.notna(closed_date):
            closed_date = closed_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            closed_date = None

        if pd.notna(created_on):
            created_on = created_on.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_on = None

        # Insert new ticket without vector
        execute_values(cur,
            """
            INSERT INTO hx_helpdesktickets_fordupli(ticket_id, company_name, problem_category, problem_sub_category, channel, closed_date, created_on, subject, description, type, space, equipment, issue_type, maintenance_team, priority, status, sla_status, ticket_type, region, actual_duration)
            VALUES %s ON CONFLICT (ticket_id) DO NOTHING
            """, 
           [(str(row['Ticket ID']), row['Company_name'], row['Problem Category'], row['Problem Sub Category'], row['Channel'], closed_date, created_on, row['Subject'], row['Description'], row['Type'], row['Space'], row['Equipment'], row['Issue Type'], row['Maintenance Team'], row['Priority'], row['Status'], row['SLA Status'], row['Ticket Type'], row['Region'], row['Actual Duration'])]
        )
        
    conn.commit()
    cur.close()
    conn.close()

# Main function for initializing the database
def initialize_db():
    # Load and preprocess data
    data = load_data(CSV_FILES)
    processed_data = preprocess_data(data)

    # Create the PostgreSQL table without vector
    create_table()

    # Insert the tickets into the database
    insert_new_ticket(processed_data)

if __name__ == "__main__":
    initialize_db()
