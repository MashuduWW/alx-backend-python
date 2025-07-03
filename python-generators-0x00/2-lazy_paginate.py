import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database.
    Returns a list of rows starting at the given offset.
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator that yields one page of users at a time using lazy loading.
    """
    offset = 0
    while True:  # Single loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
