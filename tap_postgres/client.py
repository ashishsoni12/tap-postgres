 
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Any, Dict
#LOGGER = singer.get_logger()
def create_postgres_engine(config) -> Any:
    """Create a SQLAlchemy engine for PostgreSQL."""
    db_url = f"postgresql+psycopg2://{config.get('user')}:{config.get('password')}@" \
             f"{config.get('host')}:{config.get('port')}/{config.get('database')}"
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1;"))
#            LOGGER.info("connection succcessfull")
        return engine
    except SQLAlchemyError as e:
#        LOGGER.info("connection unsucccessfull")
        raise

