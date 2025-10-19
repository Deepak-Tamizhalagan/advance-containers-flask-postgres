import os
import psycopg

def get_conn():
    """
    Return a new psycopg connection using env vars.
    In Docker we'll pass these via .env / compose.
    """
    return psycopg.connect(
        dbname=os.getenv("POSTGRES_DB", "appdb"),
        user=os.getenv("POSTGRES_USER", "appuser"),
        password=os.getenv("POSTGRES_PASSWORD", "changeme"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        autocommit=True,   # keep it simple for this assignment
    )
