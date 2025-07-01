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
    INSERT INTO event_applications(event_id, performer_id, status, applied_at)
    VALUES (p_event_id, p_performer_id, 'pending', NOW())
    RETURNING event_applications.id, event_applications.event_id, event_applications.performer_id, event_applications.status, event_applications.applied_at;
END;
$$;
