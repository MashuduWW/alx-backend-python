import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    
    for (age,) in cursor:  # 1st loop
        yield float(age)
    
    cursor.close()
    connection.close()

def calculate_average_age():
    """
    Calculates and prints the average age using the stream_user_ages generator.
    """
    total = 0
    count = 0
    for age in stream_user_ages():  # 2nd loop
        total += age
        count += 1
    if count == 0:
        print("No users found.")
    else:
        print(f"Average age of users: {total / count:.2f}")

if __name__ == "__main__":
    calculate_average_age()
