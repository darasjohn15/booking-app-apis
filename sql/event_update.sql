CREATE OR REPLACE FUNCTION Event_UPDATE(
    p_id INTEGER,
    p_title VARCHAR DEFAULT NULL,
    p_date TIMESTAMP DEFAULT NULL,
    p_venue_id INTEGER DEFAULT NULL,
    p_description TEXT DEFAULT NULL,
    p_is_active BOOLEAN DEFAULT NULL
)
RETURNS TABLE (
    id INTEGER,
    host_id INTEGER,
    venue_id INTEGER,
    title VARCHAR,
    description TEXT,
    location VARCHAR,
    date TIMESTAMP,
    created_at TIMESTAMP,
    is_active BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE events
    SET
        title = COALESCE(p_title, title),
        date = COALESCE(p_date, date),
        venue_id = COALESCE(p_venue_id, venue_id),
        description = COALESCE(p_description, description),
        is_active = COALESCE(p_is_active, is_active)
    WHERE id = p_id;

    RETURN QUERY
    SELECT * FROM events WHERE id = p_id;
END;
$$;
