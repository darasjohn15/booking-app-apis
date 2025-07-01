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
        event_applications.id,
        event_applications.event_id,
        event_applications.performer_id,
        event_applications.status,
        event_applications.applied_at
    FROM event_applications
    WHERE event_applications.id = p_id;
END;
$$;
