from flask import Flask, jsonify
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Define the analysis function
def analyze():
    # Connect to PostgreSQL using credentials from .env
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    # Fetch data from the database
    query = "SELECT * FROM public.hx_helpdesk_tickets"
    df = pd.read_sql_query(query, conn)

    # Debug: Print the shape of the filtered data
    print(f"Filtered data shape: {df.shape}")

    # Filter data for SLA Elapsed
    sla_elapsed_df = df[df['sla_status'] == 'SLA Elapsed']

    # Calculate overall SLA compliance rate
    sla_compliance_rate = round((df['sla_status'] != 'SLA Elapsed').mean() * 100, 2)

    # Identify and extract relevant factors impacting SLA compliance
    relevant_factors = ['problem_category', 'problem_subcategory', 'maintenance_team']
    analysis_results = {
        'sla_compliance_rate': sla_compliance_rate,
        'top_10_factors': {},
        'maintenance_team_problem_categories': {},
        'company_sla_elapsed_counts': {},
        'maintenance_team_company_counts': {}
    }

    for factor in relevant_factors:
        # Calculate SLA Elapsed instances grouped by factor
        sla_elapsed_counts = sla_elapsed_df.groupby(factor).size().sort_values(ascending=False)

        # Display only the top 10 entries
        top_10 = sla_elapsed_counts.head(10)
        analysis_results['top_10_factors'][factor] = top_10.to_dict()

        # For Maintenance Team, also show which Problem Categories have SLA Elapsed
        if factor == 'maintenance_team':
            analysis_results['maintenance_team_problem_categories'] = {}
            for team in top_10.index:
                team_df = sla_elapsed_df[sla_elapsed_df['maintenance_team'] == team]
                problem_categories = team_df['problem_category'].value_counts().sort_values(ascending=False)
                analysis_results['maintenance_team_problem_categories'][team] = problem_categories.to_dict()

    # Calculate SLA non-compliance counts by company
    company_sla_elapsed_counts = sla_elapsed_df['company'].value_counts().sort_values(ascending=False)
    analysis_results['company_sla_elapsed_counts'] = company_sla_elapsed_counts.to_dict()

    # Calculate Maintenance Team SLA non-compliance counts by company
    maintenance_team_company_counts = sla_elapsed_df.groupby(['maintenance_team', 'company'], dropna=False).size().sort_values(ascending=False)
    maintenance_team_company_counts_dict = {}
    for (team, company), count in maintenance_team_company_counts.items():
        if team not in maintenance_team_company_counts_dict:
            maintenance_team_company_counts_dict[team] = {}
        maintenance_team_company_counts_dict[team][company] = count
    analysis_results['maintenance_team_company_counts'] = maintenance_team_company_counts_dict

    # Close the connection
    conn.close()

    return analysis_results

# Define the API route
@app.route('/api/perform-analysis', methods=['GET'])
def perform_analysis():
    try:
        results = analyze()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
