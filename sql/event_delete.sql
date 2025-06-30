-- events_delete.sql
-- Deletes an event by ID and returns the deleted row

CREATE OR REPLACE FUNCTION Event_DELETE(
    p_event_id INTEGER
)
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
    DELETE FROM events
    WHERE events.id = p_event_id
    RETURNING events.id, events.host_id, events.title, events.description,
              events.location, events.date, events.created_at;
END;
$$ LANGUAGE plpgsql;
