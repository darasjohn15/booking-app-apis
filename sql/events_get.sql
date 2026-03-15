CREATE OR REPLACE FUNCTION Events_GET(
    p_host_id INTEGER DEFAULT NULL,
    p_active BOOLEAN DEFAULT NULL,
    p_location VARCHAR DEFAULT NULL,
    p_venue_id INTEGER DEFAULT NULL,
    p_date_start TIMESTAMP DEFAULT NULL,
    p_date_end TIMESTAMP DEFAULT NULL,
    p_page INTEGER DEFAULT 1,
    p_page_size INTEGER DEFAULT 6
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
    is_active BOOLEAN,
    total_count BIGINT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_offset INTEGER;
BEGIN
    -- Calculate pagination offset
    v_offset := (GREATEST(p_page, 1) - 1) * GREATEST(p_page_size, 1);

    RETURN QUERY
    SELECT
        e.id,
        e.host_id,
        e.venue_id,
        e.title,
        e.description,
        e.location,
        e.date,
        e.created_at,
        e.is_active,

        -- Window function gives total number of filtered rows
        COUNT(*) OVER() AS total_count

    FROM events e

    WHERE
        (p_host_id IS NULL OR e.host_id = p_host_id) AND
        (p_active IS NULL OR e.is_active = p_active) AND
        (p_location IS NULL OR e.location = p_location) AND
        (p_venue_id IS NULL OR e.venue_id = p_venue_id) AND
        (p_date_start IS NULL OR e.date >= p_date_start) AND
        (p_date_end IS NULL OR e.date <= p_date_end)

    ORDER BY
        e.date ASC,
        e.id ASC

    LIMIT GREATEST(p_page_size, 1)
    OFFSET v_offset;
END;
$$;