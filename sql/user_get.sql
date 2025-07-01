CREATE OR REPLACE FUNCTION User_GET(p_id INTEGER)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    password_hash TEXT,
    role VARCHAR,
    created_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT  users.id, 
            users.name, 
            users.email, 
            users.password_hash, 
            users.role, 
            users.created_at
    FROM users
    WHERE users.id = p_id;
END;
$$;
