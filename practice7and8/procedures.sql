CREATE OR REPLACE PROCEDURE public.insert_user(
    IN p_first_name VARCHAR(100), 
    IN p_last_name VARCHAR(100), 
    IN p_phone_number VARCHAR(20))
LANGUAGE plpgsql
AS $$

BEGIN
    INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (p_first_name, p_last_name, p_phone_number)
    ON CONFLICT (first_name, last_name) DO UPDATE SET phone_number = EXCLUDED.phone_number;
END;
$$;