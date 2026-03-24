import os
import psycopg2
import bcrypt
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def get_or_create_user(cur, name: str, email: str, password: str, role: str) -> int:
    cur.execute("SELECT id FROM users WHERE email = %s;", (email,))
    existing = cur.fetchone()
    if existing:
        return existing[0]

    password_hash = hash_password(password)

    cur.execute(
        """
        INSERT INTO users (name, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (name, email, password_hash, role),
    )
    return cur.fetchone()[0]


def get_or_create_event(cur, user_id: int, title: str, description: str, location: str, date: str) -> int:
    cur.execute(
        """
        SELECT id
        FROM events
        WHERE user_id = %s AND title = %s AND date = %s;
        """,
        (user_id, title, date),
    )
    existing = cur.fetchone()
    if existing:
        return existing[0]

    cur.execute(
        """
        INSERT INTO events (user_id, title, description, location, date)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (user_id, title, description, location, date),
    )
    return cur.fetchone()[0]


def create_application_if_missing(cur, event_id: int, performer_id: int, status: str = "pending") -> None:
    cur.execute(
        """
        SELECT id
        FROM applications
        WHERE event_id = %s AND performer_id = %s;
        """,
        (event_id, performer_id),
    )
    existing = cur.fetchone()
    if existing:
        return

    cur.execute(
        """
        INSERT INTO applications (event_id, performer_id, status)
        VALUES (%s, %s, %s);
        """,
        (event_id, performer_id, status),
    )


def seed_data():
    conn = get_db_connection()
    cur = conn.cursor()

    # Users
    host_id = get_or_create_user(
        cur,
        name="Host King",
        email="host@example.com",
        password="password123",
        role="host",
    )

    performer_id = get_or_create_user(
        cur,
        name="Performer Diva",
        email="performer@example.com",
        password="password123",
        role="performer",
    )

    # Events
    rooftop_event_id = get_or_create_event(
        cur,
        user_id=host_id,
        title="Rooftop Vibes",
        description="A sunset rooftop party with DJs and live performers.",
        location="Atlanta, GA",
        date="2026-04-01 19:00:00",
    )

    queer_night_event_id = get_or_create_event(
        cur,
        user_id=host_id,
        title="Queer Night Live",
        description="A high-energy night of drag, dance, and music.",
        location="Atlanta, GA",
        date="2026-04-05 21:00:00",
    )

    # Application
    create_application_if_missing(
        cur,
        event_id=rooftop_event_id,
        performer_id=performer_id,
        status="pending",
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed_data()