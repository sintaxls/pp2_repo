CREATE OR REPLACE PROCEDURE public.insert_user(
    IN p_first_name VARCHAR(100), 
    IN p_last_name VARCHAR(100), 
    IN p_phone_number VARCHAR(20))
LANGUAGE plpgsql
AS $$

BEGIN
    INSERT INTO phonebook (first_name, last_name, phone_number)
    VALUES (p_first_name, p_last_name, p_phone_number)
    ON CONFLICT (phone_number)
    DO UPDATE
    SET first_name = EXCLUDED.first_name,
        last_name = EXCLUDED.last_name;
END;
$$;

CREATE OR REPLACE PROCEDURE public.insert_many_users(
    IN p_users JSONB,
    INOUT p_invalid_rows JSONB DEFAULT '[]'::jsonb
)
LANGUAGE plpgsql
AS $$
DECLARE
    user_item JSONB;
    v_first_name VARCHAR(100);
    v_last_name VARCHAR(100);
    v_phone_number VARCHAR(20);

BEGIN
    FOR user_item IN SELECT value FROM jsonb_array_elements(p_users)
    LOOP
        v_first_name := user_item->>'first_name';
        v_last_name := user_item->>'last_name';
        v_phone_number := user_item->>'phone_number';

        IF v_first_name IS NULL OR btrim(v_first_name) = ''
           OR v_last_name IS NULL OR btrim(v_last_name) = ''
           OR v_phone_number IS NULL
           OR v_phone_number !~ '^\+?[0-9 ]{10,20}$'
        THEN
            p_invalid_rows := p_invalid_rows || jsonb_build_array(
                jsonb_build_object(
                    'first_name', v_first_name,
                    'last_name', v_last_name,
                    'phone_number', v_phone_number,
                    'reason', 'Invalid name or phone'
                )
            );
        ELSE
            INSERT INTO phonebook (first_name, last_name, phone_number)
            VALUES (v_first_name, v_last_name, v_phone_number)
            ON CONFLICT (phone_number)
            DO UPDATE
            SET first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name;
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE public.delete_by_id_or_phone(
    IN p_id INT DEFAULT NULL,
    IN p_phone VARCHAR(20) DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_id IS NOT NULL THEN
        DELETE FROM phonebook
        WHERE id = p_id;

    ELSIF p_phone IS NOT NULL AND btrim(p_phone) <> '' THEN
        DELETE FROM phonebook
        WHERE phone_number = p_phone;

    ELSE
        RAISE EXCEPTION 'Provide either id or phone number';
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE public.add_phone(
    IN p_contact_name VARCHAR,
    IN p_phone VARCHAR,
    IN p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id
    INTO v_contact_id
    FROM phonebook
    WHERE first_name || ' ' || last_name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'contact not found';
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE public.move_to_group(
    IN p_contact_name VARCHAR,
    IN p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INT;
BEGIN
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id
    INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE phonebook
    SET group_id = v_group_id
    WHERE first_name || ' ' || last_name = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'contact not found';
    END IF;
END;
$$;

-- TO APPLY THE CHANGES: \i practice7and8/procedures.sql
