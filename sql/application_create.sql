CREATE OR REPLACE FUNCTION Application_CREATE(
    p_event_id INTEGER,
    p_performer_id INTEGER
)
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
    INSERT INTO applications(event_id, performer_id, status, applied_at)
    VALUES (p_event_id, p_performer_id, 'pending', NOW())
    RETURNING applications.id, applications.event_id, applications.performer_id, applications.status, applications.applied_at;
END;
$$;
