"""
Module to connect to a DuckDB database and process energy consumption data.
"""

import duckdb
import pandas as pd
import datetime
from datetime import datetime

def load_and_process_data():
        """
        Connects to a DuckDB database, retrieves and processes energy consumption data.

        Returns:
        pd.DataFrame: Processed DataFrame containing hourly energy consumption data.
        """

        conn = duckdb.connect("./energy_db.db")




        result = conn.execute("SELECT * FROM energy_hourly")
        df_energy = result.fetch_df()

        result2 = conn.execute("SELECT * FROM weather_hour")
        dz_hour=result2.fetch_df()

        

        # Convert date_time column to datetime if not already

        return df_energy,dz_hour
