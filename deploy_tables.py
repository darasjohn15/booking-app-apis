import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Connect to Supabase Postgres using environment variables."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", 5432)
    )
    return conn

def deploy_tables():
    """Create tables in the correct order with constraints."""
    conn = get_db_connection()
    cur = conn.cursor()

    # 1. Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role VARCHAR NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT now()
        );
    """)

    # 2. Events table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            title VARCHAR NOT NULL,
            description TEXT,
            location VARCHAR,
            date TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT now()
        );
    """)

    # 3. Applications table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id SERIAL PRIMARY KEY,
            event_id INTEGER NOT NULL REFERENCES events(id),
            performer_id INTEGER NOT NULL REFERENCES users(id),
            status VARCHAR NOT NULL,
            applied_at TIMESTAMP DEFAULT now()
        );
    """)

    # 4. Venues table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS venues (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL
        );
    """)

    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()
    print("Tables deployed successfully!")

if __name__ == "__main__":
    deploy_tables()
