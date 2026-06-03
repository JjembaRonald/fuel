import os
from contextlib import contextmanager
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

# Load environment variables
load_dotenv()


class DatabaseManager:

    def __init__(self):
        self.db_host = os.getenv("DB_HOST")
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_port = os.getenv("DB_PORT")

        if not self.db_password:
            raise ValueError(
                "CRITICAL: DB_PASSWORD is not set in the environment variables."
            )

    def _get_connection(self):
        #Creates and returns a raw PostgreSQL connection.
        return psycopg.connect(
            host=self.db_host,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            port=self.db_port
        )

    @contextmanager
    def get_cursor(self):
        # To ensure clean handling of cursors and transactions.
        conn = self._get_connection()
        
        # RealDictCursor returns rows as native Python dicts instead of tuples
        cursor = conn.cursor(row_factory=dict_row)
        try:
            yield cursor
            conn.commit()
        except Exception as error:
            conn.rollback()
            raise error
        finally:
            cursor.close()
            conn.close()


# Instantiate a global connection manager
db = DatabaseManager()
