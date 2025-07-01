CREATE OR REPLACE FUNCTION User_UPDATE(
    p_id INTEGER,
    p_name VARCHAR DEFAULT NULL,
    p_email VARCHAR DEFAULT NULL,
    p_password_hash TEXT DEFAULT NULL,
    p_role VARCHAR DEFAULT NULL
)
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
    UPDATE users
    SET
        name = COALESCE(p_name, users.name),
        email = COALESCE(p_email, users.email),
        password_hash = COALESCE(p_password_hash, users.password_hash),
        role = COALESCE(p_role, users.role)
    WHERE users.id = p_id
    RETURNING users.id, users.name, users.email, users.password_hash, users.role, users.created_at;
END;
$$;
