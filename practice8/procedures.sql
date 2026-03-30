CREATE OR REPLACE PROCEDURE upsert_contact(p_username VARCHAR, p_surname VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_username AND surname = p_surname) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE username = p_username AND surname = p_surname;
    ELSE
        INSERT INTO phonebook(username, surname, phone)
        VALUES(p_username, p_surname, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts()
LANGUAGE plpgsql AS $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN SELECT * FROM temp_contacts LOOP
        IF length(rec.phone) >= 10 THEN
            INSERT INTO phonebook(username, surname, phone)
            VALUES(rec.username, rec.surname, rec.phone)
            ON CONFLICT (phone) DO NOTHING;
        ELSE
            RAISE NOTICE 'Invalid phone: %', rec.phone;
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_username VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_username IS NOT NULL THEN
        DELETE FROM phonebook WHERE username = p_username;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
    END IF;
END;
$$;