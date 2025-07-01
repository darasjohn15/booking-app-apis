CREATE OR REPLACE FUNCTION Application_UPDATE(
    p_id INTEGER,
    p_status VARCHAR
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
    UPDATE event_applications
    SET status = p_status
    WHERE event_applications.id = p_id
    RETURNING event_applications.id, event_applications.event_id, event_applications.performer_id, event_applications.status, event_applications.applied_at;
END;
$$;
