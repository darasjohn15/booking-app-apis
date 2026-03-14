CREATE OR REPLACE FUNCTION Events_GET(
    p_host_id INTEGER DEFAULT NULL,
    p_active BOOLEAN DEFAULT NULL,
    p_location VARCHAR DEFAULT NULL,
    p_venue_id INTEGER DEFAULT NULL,
    p_date_start TIMESTAMP DEFAULT NULL,
    p_date_end TIMESTAMP DEFAULT NULL
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
    RETURN QUERY
    SELECT
        events.id,
        events.host_id,
        events.venue_id,
        events.title,
        events.description,
        events.location,
        events.date,
        events.created_at,
        events.is_active
    FROM events
    WHERE
        (p_host_id IS NULL OR events.host_id = p_host_id) AND
        (p_active IS NULL OR events.is_active = p_active) AND
        (p_location IS NULL OR events.location = p_location) AND
        (p_venue_id IS NULL OR events.venue_id = p_venue_id) AND
        (p_date_start IS NULL OR events.date >= p_date_start) AND
        (p_date_end IS NULL OR events.date <= p_date_end);
END;
$$;