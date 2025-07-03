import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields rows in batches from user_data table.
    Each batch is a list of dicts with batch_size items (or fewer on the last batch).
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:  # 1st loop
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Processes each batch by filtering users over the age of 25.
    Yields a filtered list of users from each batch.
    """
    for batch in stream_users_in_batches(batch_size):  # 2nd loop
        filtered = [user for user in batch if float(user['age']) > 25]  # 3rd loop
        yield filtered
