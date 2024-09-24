import psycopg2
from psycopg2 import OperationalError

# Configuration details
host = "ec2-3-0-184-69.ap-southeast-1.compute.amazonaws.com"
port = 30003
username = "watermelon"  # Update with your username
password = "watermelon123"  # Update with your password
dbname = "wmebservices"

def test_connection():
    """Test connection to the PostgreSQL database."""
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            dbname=dbname
        )
        print("Connection successful!")

        # Create a cursor object
        cursor = conn.cursor()

        # Execute a simple query to test
        cursor.execute("SELECT 1;")

        # Fetch the result
        result = cursor.fetchone()
        print("Query result:", result)

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except OperationalError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()

