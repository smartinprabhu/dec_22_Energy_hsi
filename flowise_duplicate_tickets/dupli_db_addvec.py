import pandas as pd
import numpy as np
from gensim.models import Word2Vec
import psycopg2
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

MODEL_FILE = 'word2vec_model.pkl'

# Fetch data from the database
def fetch_data_from_db():
    conn = psycopg2.connect(**DB_CONFIG)
    query = """
        SELECT ticket_id, subject, problem_category, problem_sub_category, type, space, equipment, description
        FROM hx_helpdesktickets_fordupli;
    """
    data = pd.read_sql(query, conn)
    conn.close()
    return data

# Train and save Word2Vec model
def train_and_save_word2vec_model(data):
    # Creating sentences from relevant fields
    sentences = data.apply(lambda x: [x['subject'], x['problem_category'], x['problem_sub_category'], x['type'], x['space'], x['equipment'], x['description']], axis=1).tolist()
    # Train Word2Vec model
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
    # Save model
    model.save(MODEL_FILE)

# Load Word2Vec model
def load_word2vec_model():
    if not os.path.exists(MODEL_FILE):
        return None
    return Word2Vec.load(MODEL_FILE)

# Vectorize sentence
def vectorize_sentence(model, subject, problem_category, problem_sub_category, type, space, equipment, description):
    sentence = f"{subject} {problem_category} {problem_sub_category} {type} {space} {equipment} {description}"
    words = sentence.split()
    word_vectors = [model.wv[word] for word in words if word in model.wv]
    return np.mean(word_vectors, axis=0) if word_vectors else np.zeros(model.vector_size)

# Add vector column to the table if not exists
def add_vector_column():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    # Add ticket_vector column if it doesn't exist
    cur.execute("""
        ALTER TABLE hx_helpdesktickets_fordupli
        ADD COLUMN IF NOT EXISTS ticket_vector VECTOR(100);
    """)
    conn.commit()
    cur.close()
    conn.close()

# Update tickets with vectors
def update_tickets_with_vectors(data, model):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for _, row in data.iterrows():
        ticket_vector = vectorize_sentence(model, row['subject'], row['problem_category'], row['problem_sub_category'], row['type'], row['space'], row['equipment'], row['description'])
        
        # Update the ticket with the generated vector
        cur.execute("""
            UPDATE hx_helpdesktickets_fordupli
            SET ticket_vector = %s
            WHERE ticket_id = %s
        """, (ticket_vector.tolist(), row['ticket_id']))

    conn.commit()
    cur.close()
    conn.close()

# Main function for processing
def process_and_update_vectors():
    # Fetch data from the database
    data = fetch_data_from_db()

    # Add vector column if not exists
    add_vector_column()

    # Train and save Word2Vec model
    train_and_save_word2vec_model(data)

    # Load Word2Vec model
    word2vec_model = load_word2vec_model()
    if word2vec_model:
        # Update tickets with vector data
        update_tickets_with_vectors(data, word2vec_model)
    else:
        print("Word2Vec model not found!")

if __name__ == "__main__":
    process_and_update_vectors()
