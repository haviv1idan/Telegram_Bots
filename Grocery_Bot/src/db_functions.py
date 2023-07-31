import sqlite3

import pandas as pd

DB_PATH = 'products_database.db'


def connect_to_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    return connection, cursor


def close_connection(connection):
    connection.close()


def create_table(conn, table_name: str, keys: list[str]) -> None:
    """
    Create a new table in the database if not already existing

    :param conn: database connection
    :param table_name: str - name of the table
    :param keys: list of strings - table columns
    :return: None
    """
    # Create a table with the specified keys
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {", ".join(keys)}
        );
    '''
    conn.execute(create_table_query)


def insert_data(conn, table_name: str, data: list[str]) -> None:
    # Insert data into the specified table
    insert_query = f'''
        INSERT INTO {table_name} VALUES ({", ".join(["?"] * len(data))})
    '''
    conn.execute(insert_query, data)
    conn.commit()


# def check_if_data_already_exist(conn, table_name: str, data: dict[str, str]):
#     """
#     Check if the specified table contains the specified data
#
#     :param conn: connection to the database
#     :param table_name: str - name of the table
#     :param data: dict of col name and data
#     :return: None, if all data is existed in table. otherwise, replace data
#     """
#     df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
#     product_id = data[HEBREW_PRODUCT_ID]
#     df_filtered_by_product_id = df[df[HEBREW_PRODUCT_ID] == product_id]
#     for key, value in data.items():
#         if key == HEBREW_PRODUCT_ID:
#             continue
#         pass
