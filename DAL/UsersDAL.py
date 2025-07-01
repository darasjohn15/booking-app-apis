from db import get_db_connection
from psycopg2.extras import RealDictCursor

def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM User_GET(%s);", (user_id,))
    event = cur.fetchone()
    cur.close()
    conn.close()
    return event

def create_user(name, email, password_hash, role):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM User_CREATE(%s, %s, %s, %s);", 
                (name, email, password_hash, role))

    new_event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return new_event

def update_user(id, name=None, email=None, password_hash=None, role=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute(
        "SELECT * FROM User_UPDATE(%s, %s, %s, %s, %s);",
        (id, name, email, password_hash, role)
    )
    
    updated_event = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return updated_event