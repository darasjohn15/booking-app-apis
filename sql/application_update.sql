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
    UPDATE applications
    SET status = p_status
    WHERE applications.id = p_id
    RETURNING applications.id, applications.event_id, applications.performer_id, applications.status, applications.applied_at;
END;
$$;
