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
            result = conn.execute("SELECT 1;")
            print(f"Connection successful! Result: {result.fetchone()}")
            
        return engine
    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")

# Example usage
connect_sqlalchemy()

