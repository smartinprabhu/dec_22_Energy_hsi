import duckdb
import pandas as pd


def create_duckdb_connection(db_file: str) -> duckdb.DuckDBPyConnection:
    """
    Connect to a DuckDB database.

    Args:
        db_file (str): The file path to the DuckDB database.

    Returns:
        duckdb.DuckDBPyConnection: A connection object to the DuckDB database.

    """
    return duckdb.connect(db_file)

def read_excel_file(file_path: str) -> pd.DataFrame:
    """
    Read an Excel file into a Pandas DataFrame.

    Args:
        file_path (str): The file path to the Excel file.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the data from the Excel file.


    """
    return pd.read_excel(file_path)

def create_table_from_dataframe(conn: duckdb.DuckDBPyConnection, df: pd.DataFrame, table_name: str) -> None:
    """
    Create a table in the DuckDB database from a Pandas DataFrame.

    Args:
        conn (duckdb.DuckDBPyConnection): A connection object to the DuckDB database.
        df (pd.DataFrame): The Pandas DataFrame to create the table from.
        table_name (str): The name of the table to create.

    Returns:
        None


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

    """
    result = conn.execute("SHOW TABLES")
    return [table[0] for table in result.fetchall()]


# Connect to the DuckDB database
conn = create_duckdb_connection('sw.db')

# Read the Excel files into Pandas DataFrames
excel_file = '/Users/vigneshk/noc/hsense-noc-frontend/smart/reading_history_FSB.csv'

pplin= pd.read_csv(excel_file)

iaqz_data = pplin[pplin['alias_name'] == 'IAQ']
pplin_delta_data = pplin[pplin['alias_name'] == 'pplin_delta']
pplin_delta_data = pplin_delta_data[pplin_delta_data['asset_number'] == 'FSMBLR-A-00002']


# Create tables in the DuckDB database from the DataFrames
create_table_from_dataframe(conn, pplin_delta_data, 'pplin')
create_table_from_dataframe(conn, iaqz_data, 'iaqz')


# List all the tables in the database
tables = list_tables(conn)
print(tables)

# Close the connection to the database
conn.close()