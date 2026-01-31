import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT", 5432)

    # Fail fast if env vars are missing
    if not all([host, dbname, user, password]):
        raise RuntimeError("Missing one or more required DB environment variables")

    try:
        return psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port,
            sslmode="require",
            connect_timeout=5,
            cursor_factory=RealDictCursor,
        )
    except psycopg2.OperationalError as e:
        # Log safely (no password, no full DSN)
        print(f"DB connection failed → host={host}, db={dbname}, user={user}")
        raise