CREATE OR REPLACE FUNCTION public.search_records(search_pattern VARCHAR(100))
RETURNS TABLE (
    id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone_number
    FROM phonebook p
    WHERE p.first_name ILIKE '%' || search_pattern || '%'
       OR p.last_name ILIKE '%' || search_pattern || '%'
       OR p.phone_number ILIKE '%' || search_pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- TO APPLY THE CHANGES: psql -U postgres -d phonebook_db -f practice7and8/functions.sql