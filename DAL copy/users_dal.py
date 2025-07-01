from db import get_db_connection
from psycopg2.extras import RealDictCursor

def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM User_GET(%s);", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def get_users(name=None, email=None, role=None, is_active=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM Users_GET(%s, %s, %s, %s);", (name, email, role, is_active))
    users = cur.fetchall()
    cur.close()
    conn.close()

    return users

def create_user(name, email, password_hash, role):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM User_CREATE(%s, %s, %s, %s);", 
                (name, email, password_hash, role))

    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return user

def update_user(id, name=None, email=None, password_hash=None, role=None, is_active=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute(
        "SELECT * FROM User_UPDATE(%s, %s, %s, %s, %s, %s);",
        (id, name, email, password_hash, role, is_active)
    )
    
    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return updated_user