from db import get_db_connection
from psycopg2.extras import RealDictCursor

def get_event(event_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Event_GET(%s);", (event_id,))
    event = cur.fetchone()
    cur.close()
    conn.close()
    return event

def get_events(host_id=None, active=None, location=None, venue_id=None, date_start=None, date_end=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Events_GET(%s, %s, %s, %s, %s, %s);", (host_id, active, location, venue_id, date_start, date_end))
    events = cur.fetchall()
    cur.close()
    conn.close()

    return events

def create_event(host_id, venue_id, title, description, location, date):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM Event_CREATE(%s, %s, %s, %s, %s, %s);", 
                (host_id, venue_id, title, description, location, date))

    new_event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return new_event

def update_event(event_id, title=None, date=None, venue_id=None, description=None, is_active=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute(
        "SELECT * FROM Event_UPDATE(%s, %s, %s, %s, %s, %s);",
        (event_id, title, date, venue_id, description, is_active)
    )
    
    updated_event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return updated_event