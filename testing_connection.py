import mysql.connector
from mysql.connector import Error

connection = None

try:
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(
        host='tuya.mysql.pythonanywhere-services.com',
        user='tuya',
        password='tuyadatabases',
        database='tuya$test-bot-prod'
    )

    if connection.is_connected():
        print("Connected to the database")
        # Example query execution
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        print("Tables:", cursor.fetchall())

except Error as e:
    print(f"Error: {e}")

finally:
    # Ensure the connection is closed
    if connection is not None and connection.is_connected():
        connection.close()
        print("Connection closed")
