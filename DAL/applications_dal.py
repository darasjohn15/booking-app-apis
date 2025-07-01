from db import get_db_connection
from psycopg2.extras import RealDictCursor

def get_application(application_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Application_GET(%s);", (application_id,))
    event = cur.fetchone()
    cur.close()
    conn.close()
    return event

def get_applications(event_id=None, performer_id=None, status=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Applications_GET(%s, %s, %s);", (event_id, performer_id, status))
    events = cur.fetchall()
    cur.close()
    conn.close()

    return events

def create_application(event_id, performer_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM Application_CREATE(%s, %s);", 
                (event_id, performer_id))

    new_event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return new_event

def update_application(id, status):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute(
        "SELECT * FROM Application_UPDATE(%s, %s);",
        (id, status)
    )
    
    updated_event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return updated_event