import sqlite3


DB_PATH = 'products_database.db'

__all__ = (
    'connect_to_db',
    'create_table',
    'insert_data',
    'delete_product',
    'swap_dict_keys',
)


def connect_to_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    return connection, cursor


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


def delete_product(conn, table_name: str, product_id: str) -> None:
    delete_query = f"DELETE FROM {table_name} WHERE barcode = '{product_id}'"
    conn.execute(delete_query)
    conn.commit()


def swap_dict_keys(dictionary, key_mapping):
    """
    Swaps the keys of a dictionary with new keys according to the provided mapping.

    Parameters:
        dictionary (dict): The original dictionary.
        key_mapping (dict): A dictionary containing the mapping of old keys to new keys.

    Returns:
        dict: The modified dictionary with swapped keys.
    """
    swapped_dict = {}
    for old_key, new_key in key_mapping.items():
        if old_key in dictionary:
            swapped_dict[new_key] = dictionary[old_key]
    return swapped_dict
