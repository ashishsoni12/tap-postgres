from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def connect_sqlalchemy():
    """Connect to PostgreSQL using SQLAlchemy."""
    try:
        engine = create_engine(
            "postgresql+psycopg2://watermelon:watermelon123@ec2-3-0-184-69.ap-southeast-1.compute.amazonaws.com:30003/wmebservices"
        )

        # Test the connection
        with engine.connect() as conn:
            result = conn.execute("""
                SELECT * 
                FROM public.test 
                WHERE data_uploaded_time >= '2024-09-13T00:00:00' 
                AND data_uploaded_time < '2024-09-20T00:00:00';
            """)
            rows = result # Fetch all records
            
#            print(f"Connection successful! Total records fetched: {len(rows)}")
            if rows:
                print("First record:", rows[0])
            else:
                print("No records found.")

            # Print all records for debugging
            print("All records fetched:")
            for row in rows:
                print(row)

        return engine
    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")

# Example usage
connect_sqlalchemy()

