CREATE OR REPLACE FUNCTION Application_GET(p_id INTEGER)
RETURNS TABLE (
    id INTEGER,
    event_id INTEGER,
    performer_id INTEGER,
    status VARCHAR,
    applied_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        applications.id,
        applications.event_id,
        applications.performer_id,
        applications.status,
        applications.applied_at
    FROM applications
    WHERE applications.id = p_id;
END;
$$;
