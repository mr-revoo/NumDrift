import psycopg2.pool
import os
import logging
from dotenv import load_dotenv, find_dotenv
from contextlib import contextmanager

logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  
        logging.FileHandler('database.log')  
    ]
)

logger = logging.getLogger(__name__)

class InitDB:
    def __init__(self):
        logger.debug("Initializing InitDB class")
        dotenv_path = find_dotenv()
        if not dotenv_path:
            logger.error("No .env file found")
            raise ValueError("No .env file found")
        load_dotenv(dotenv_path)
        logger.debug(f"Loaded .env file from {dotenv_path}")

        db_url = os.getenv("DB_URL")
        if not db_url:
            logger.error("DB_URL not found in environment variables")
            raise ValueError("DB_URL not found in environment variables. Ensure .env file is set up correctly.")
        logger.debug("DB_URL loaded successfully")

        try:
            self.pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=15,
                dsn=db_url
            )
            logger.info("Database connection pool created successfully")
        except psycopg2.Error as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise RuntimeError(f"Failed to create connection pool: {e}")

    def get_connection(self):
        """Get a raw connection from the pool."""
        
        try:
            conn = self.pool.getconn()
            logger.info("Successfully retrieved connection from pool")
            return conn
        except psycopg2.Error as e:
            logger.error(f"Failed to get connection from pool: {e}")
            raise RuntimeError(f"Failed to get connection from pool: {e}")

    @contextmanager
    def get_cursor(self):
        """Provide a cursor for executing queries, automatically managing the connection."""
        logger.debug("Requesting cursor via context manager")
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction failed, rolled back: {e}")
            raise
        finally:
            logger.debug("Returning connection to pool")
            self.pool.putconn(conn)
            logger.info("Connection returned to pool")