"""
Module to connect to a DuckDB database and process smart-washroom data.
"""

import duckdb
import pandas as pd


def load_and_process_data():
    """
    Connects to a DuckDB database, retrieves and processes smart-washroom data.

    Returns:
    pd.DataFrame: Processed DataFrame containing hourly smart-washroom data.
    """
    # Connect to the DuckDB database
    # We assume that the database file is named "my_database.db" and is
    # located in the current working directory
    conn = duckdb.connect("./sw.db")

    # Execute a SQL query to select all data from the 'energy_data' table
    # The 'energy_data' table is assumed to have two columns: 'ds' (datetime)
  
    result = conn.execute("SELECT * FROM pplin")
    pplin = result.fetch_df()
    result1 = conn.execute("SELECT * FROM iaqz")
    iaqz = result1.fetch_df()


    pplin['measured_ts'] = pd.to_datetime(pplin['measured_ts'], errors='coerce')


    pplin = pplin[['measured_ts','answer_value']].set_index("measured_ts").resample('H').sum()


    return pplin,iaqz