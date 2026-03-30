CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, username VARCHAR, surname VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.username, p.surname, p.phone
    FROM phonebook p
    WHERE p.username ILIKE '%' || pattern || '%'
       OR p.surname ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(id INT, username VARCHAR, surname VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT id, username, surname, phone
    FROM phonebook
    ORDER BY id
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;


