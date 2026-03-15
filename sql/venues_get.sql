CREATE OR REPLACE FUNCTION Venues_GET()
RETURNS TABLE (
    id INTEGER,
    name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        v.id,
        v.name
    FROM venues v;

END;
$$;