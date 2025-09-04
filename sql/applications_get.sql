CREATE OR REPLACE FUNCTION Applications_GET(
    p_event_id INTEGER DEFAULT NULL,
    p_performer_id INTEGER DEFAULT NULL,
    p_status VARCHAR DEFAULT NULL
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
    SELECT *
    FROM applications
    WHERE
        (p_event_id IS NULL OR applications.event_id = p_event_id) AND
        (p_performer_id IS NULL OR applications.performer_id = p_performer_id) AND
        (p_status IS NULL OR applications.status = p_status);
END;
$$;
