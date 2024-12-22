import duckdb
import pandas as pd

def create_duckdb_connection(db_file: str) -> duckdb.DuckDBPyConnection:
    """
    Connect to a DuckDB database.

    Args:
        db_file (str): The file path to the DuckDB database.

    Returns:
        duckdb.DuckDBPyConnection: A connection object to the DuckDB database.

    Example:
        conn = create_duckdb_connection('my_database.db')
    """
    return duckdb.connect(db_file)

def read_csv_file(file_path: str) -> pd.DataFrame:

    return pd.read_csv(file_path)

def create_table_from_dataframe(conn: duckdb.DuckDBPyConnection, df: pd.DataFrame, table_name: str) -> None:
    """
    Create a table in the DuckDB database from a Pandas DataFrame.

    Args:
        conn (duckdb.DuckDBPyConnection): A connection object to the DuckDB database.
        df (pd.DataFrame): The Pandas DataFrame to create the table from.
        table_name (str): The name of the table to create.

    Returns:
        None

    Example:
        create_table_from_dataframe(conn, df, 'weather_data')
    """
    create_table_query = f"CREATE TABLE {table_name} AS SELECT * FROM df"
    conn.execute(create_table_query)

def list_tables(conn: duckdb.DuckDBPyConnection) -> list:
    """
    List all the tables in the DuckDB database.

    Args:
        conn (duckdb.DuckDBPyConnection): A connection object to the DuckDB database.

    Returns:
        list: A list of table names in the database.

    Example:
        tables = list_tables(conn)
        print(tables)
    """
    result = conn.execute("SHOW TABLES")
    return [table[0] for table in result.fetchall()]

# Connect to the DuckDB database


conn = duckdb.connect("energy_db.db")

# Read the Excel files into Pandas DataFrames
excel_file = '/Users/vigneshk/NOC-DASHBOARD/hsense-insights/energy/whitefield_weather_data-31-07-2024.csv'


excel_file4 = '/Users/vigneshk/NOC-DASHBOARD/hsense-insights/energy/data_energy_kwh_30-07-2024.csv'
df = pd.read_csv(excel_file)

dfy = pd.read_csv(excel_file4)
# Create tables in the DuckDB database from the DataFrames
create_table_from_dataframe(conn, df, 'weather_hour')

create_table_from_dataframe(conn, dfy, 'energy_hourly')
# List all the tables in the database
tables = list_tables(conn)
print(tables)

# Close the connection to the database
conn.close()