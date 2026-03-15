from db import get_db_connection
from psycopg2.extras import RealDictCursor

def get_venue(venue_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Venue_GET(%s);", (venue_id))
    event = cur.fetchone()
    cur.close()
    conn.close()
    return event

def get_venues():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Venues_GET();", ())
    events = cur.fetchall()
    cur.close()
    conn.close()

    return events