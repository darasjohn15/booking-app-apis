CREATE OR REPLACE FUNCTION Users_GET(
    p_name VARCHAR DEFAULT NULL,
    p_email VARCHAR DEFAULT NULL,
    p_role VARCHAR DEFAULT NULL,
    p_is_active BOOLEAN DEFAULT NULL
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
    SELECT
        users.id,
        users.name,
        users.email,
        users.password_hash,
        users.role,
        users.is_active,
        users.created_at
    FROM users
    WHERE
        (p_name IS NULL OR users.name = p_name) AND
        (p_email IS NULL OR users.email = p_email) AND
        (p_role IS NULL OR users.role = p_role) AND
        (p_is_active IS NULL OR users.is_active = p_is_active);
END;
$$;