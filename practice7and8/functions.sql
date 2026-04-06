CREATE OR REPLACE FUNCTION public.search_records(search_pattern VARCHAR(100))
RETURNS TABLE (
    id INT,
    name VARCHAR(100),
    surname VARCHAR(100),
    phone_number VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT r.id, r.name, r.surname, r.phone_number
    FROM records r
    WHERE r.name ILIKE '%' || search_pattern || '%'
       OR r.surname ILIKE '%' || search_pattern || '%'
       OR r.phone_number ILIKE '%' || search_pattern || '%';
END;
$$ LANGUAGE plpgsql;