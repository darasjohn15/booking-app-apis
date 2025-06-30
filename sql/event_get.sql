CREATE OR REPLACE FUNCTION Event_GET(p_eventID INTEGER)
RETURNS TABLE (
    id INTEGER,
    host_id INTEGER,
    title VARCHAR,
    description TEXT,
    location VARCHAR,
    date TIMESTAMP,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT e.id, e.host_id, e.title, e.description, e.location, e.date, e.created_at
    FROM events e
    WHERE e.id = p_eventID;
END;
$$ LANGUAGE plpgsql;
