CREATE OR REPLACE FUNCTION Event_CREATE(
    p_host_id INTEGER,
    p_venue_id INTEGER,
    p_title VARCHAR,
    p_description TEXT,
    p_date TIMESTAMP
)
RETURNS TABLE (
    id INTEGER,
    host_id INTEGER,
    venue_id INTEGER,
    title VARCHAR,
    description TEXT,
    date TIMESTAMP,
    created_at TIMESTAMP,
    is_active BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    INSERT INTO events (host_id, venue_id, title, description, date)
    VALUES (p_host_id, p_venue_id, p_title, p_description, p_date)
    RETURNING 
        events.id, 
        events.host_id, 
        events.venue_id,
        events.title, 
        events.description, 
        events.date, 
        events.created_at, 
        events.is_active;
END;
$$;
