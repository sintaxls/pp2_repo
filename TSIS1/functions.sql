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


CREATE OR REPLACE FUNCTION public.phonebook_paginate(
    p_limit INT,
    p_offset INT
)
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
    ORDER BY p.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.search_contacts(p_query TEXT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone_number, p.email
    FROM phonebook p
    LEFT JOIN groups g ON p.group_id = g.id
    WHERE p.first_name ILIKE '%' || p_query || '%'
       OR p.last_name ILIKE '%' || p_query || '%'
       OR p.phone_number ILIKE '%' || p_query || '%'
       OR p.email ILIKE '%' || p_query || '%'
       OR p.birthday::TEXT ILIKE '%' || p_query || '%'
       OR g.name ILIKE '%' || p_query || '%'
       OR EXISTS (
           SELECT 1
           FROM phones ph
           WHERE ph.contact_id = p.id
             AND ph.phone ILIKE '%' || p_query || '%'
       )
    ORDER BY p.id;
END;
$$ LANGUAGE plpgsql;

-- TO APPLY THE CHANGES: psql -U postgres -d phonebook_db -f practice7and8/functions.sql
