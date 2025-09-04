CREATE OR REPLACE FUNCTION Application_DELETE(p_id INTEGER)
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
    DELETE FROM applications
    WHERE applications.id = p_id
    RETURNING applications.id, applications.event_id, applications.performer_id, applications.status, applications.applied_at;
END;
$$;
