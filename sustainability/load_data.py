"""
Module to connect to a DuckDB database and process energy consumption data.
"""

import duckdb
import pandas as pd
from datetime import datetime

def load_and_process_data():
    """
    Connects to a DuckDB database, retrieves and processes energy consumption data.

    Returns:
    tuple: A tuple containing DataFrames for each table in the database.
    """

    conn = duckdb.connect("./sustainability.db")

    # Fetch data from each table individually
    result = conn.execute("SELECT * FROM DG_hour")
    DG_hour = result.fetch_df()

    result = conn.execute("SELECT * FROM EB_hour")
    EB_hour = result.fetch_df()

    result = conn.execute("SELECT * FROM solar_hour")
    solar_hour = result.fetch_df()



    result = conn.execute("SELECT * FROM h_asset1")
    h_asset1 = result.fetch_df()

    result = conn.execute("SELECT * FROM h_asset2")
    h_asset2 = result.fetch_df()

    result = conn.execute("SELECT * FROM h_asset3")
    h_asset3 = result.fetch_df()

    result = conn.execute("SELECT * FROM h_asset4")
    h_asset4 = result.fetch_df()

    result = conn.execute("SELECT * FROM h_asset5")
    h_asset5 = result.fetch_df()

    result = conn.execute("SELECT * FROM h_asset6")
    h_asset6 = result.fetch_df()

    result = conn.execute("SELECT * FROM h_asset7")
    h_asset7 = result.fetch_df()

    result = conn.execute("SELECT * FROM h_asset8")
    h_asset8 = result.fetch_df()

    result = conn.execute("SELECT * FROM h_asset9")
    h_asset9 = result.fetch_df()

    result = conn.execute("SELECT * FROM h_asset10")
    h_asset10 = result.fetch_df()

    result = conn.execute("SELECT * FROM h_asset11")
    h_asset11 = result.fetch_df()
    result = conn.execute("SELECT * FROM h_asset12")
    h_asset12 = result.fetch_df()
    result = conn.execute("SELECT * FROM h_asset13")
    h_asset13 = result.fetch_df()
    result = conn.execute("SELECT * FROM h_asset14")
    h_asset14 = result.fetch_df()
    
    result = conn.execute("SELECT * FROM l_asset1")
    l_asset1 = result.fetch_df()

    result = conn.execute("SELECT * FROM l_asset2")
    l_asset2 = result.fetch_df()

    result = conn.execute("SELECT * FROM l_asset3")
    l_asset3 = result.fetch_df()

    result = conn.execute("SELECT * FROM l_asset4")
    l_asset4 = result.fetch_df()

    result = conn.execute("SELECT * FROM l_asset5")
    l_asset5 = result.fetch_df()

    result = conn.execute("SELECT * FROM l_asset6")
    l_asset6 = result.fetch_df()

    result = conn.execute("SELECT * FROM c_asset1")
    c_asset1 = result.fetch_df()

    result = conn.execute("SELECT * FROM c_asset2")
    c_asset2 = result.fetch_df()

    result = conn.execute("SELECT * FROM c_asset3")
    c_asset3 = result.fetch_df()

    result = conn.execute("SELECT * FROM c_asset4")
    c_asset4 = result.fetch_df()

    result = conn.execute("SELECT * FROM c_asset5")
    c_asset5 = result.fetch_df()

    result = conn.execute("SELECT * FROM c_asset6")
    c_asset6 = result.fetch_df()
    result = conn.execute("SELECT * FROM c_asset7")
    c_asset7 = result.fetch_df()
    # Close the connection to the database
    conn.close()

    # Return the DataFrames
    return (
         DG_hour,  EB_hour, solar_hour,
        h_asset1, h_asset2, h_asset3, h_asset4, h_asset5, h_asset6,
        h_asset7, h_asset8, h_asset9, h_asset10, h_asset11,h_asset12,h_asset13,h_asset14,
        l_asset1, l_asset2, l_asset3, l_asset4, l_asset5, l_asset6,
        c_asset1, c_asset2, c_asset3, c_asset4, c_asset5, c_asset6,c_asset7
    )
