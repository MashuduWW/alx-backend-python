import mysql.connector
import csv
import uuid

DB_CONFIG = {
    'host': 'localhost',
    'user': 'mysql_username',
    'password': 'mysql_password'
}

def connect_db():
    """Connect to the MySQL server (without selecting a DB)."""
    return mysql.connector.connect(**DB_CONFIG)

def create_database(connection):
    """Create ALX_prodev database if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database='ALX_prodev'
    )

def create_table(connection):
    """Create user_data table if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        )
    """)
    connection.commit()
    cursor.close()

def insert_data(connection, data):
    """Insert user data if the email does not already exist."""
    cursor = connection.cursor()
    for row in data:
        name, email, age = row
        cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
        if cursor.fetchone():
            continue  # Skip if email already exists
        uid = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
            (uid, name, email, age)
        )
    connection.commit()
    cursor.close()

def read_csv(filepath):
    """Read user data from CSV file."""
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        return [row for row in reader]

if __name__ == "__main__":
    csv_file = "user_data.csv"
    initial_connection = connect_db()
    create_database(initial_connection)
    initial_connection.close()

    db_connection = connect_to_prodev()
    create_table(db_connection)
    user_data = read_csv(csv_file)
    insert_data(db_connection, user_data)
    db_connection.close()

    print("Database seeded successfully.")
