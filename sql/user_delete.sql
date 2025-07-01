CREATE OR REPLACE FUNCTION User_DELETE(p_id INTEGER)
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
    DELETE FROM users
    WHERE users.id = p_id
    RETURNING users.id, users.name, users.email, users.password_hash, users.role, users.created_at;
END;
$$;
