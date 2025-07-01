CREATE OR REPLACE FUNCTION User_CREATE(
    p_name VARCHAR,
    p_email VARCHAR,
    p_password_hash TEXT,
    p_role VARCHAR
)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    password_hash TEXT,
    role VARCHAR,
    is_active BOOLEAN,
    created_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    INSERT INTO users (name, email, password_hash, role, is_active, created_at)
    VALUES (p_name, p_email, p_password_hash, p_role, TRUE, NOW())
    RETURNING users.id, users.name, users.email, users.password_hash, users.role, users.is_active, users.created_at;
END;
$$;
