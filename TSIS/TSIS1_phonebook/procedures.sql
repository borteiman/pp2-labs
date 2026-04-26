CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_type VARCHAR;
BEGIN
    v_type := LOWER(p_type);

    IF v_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Phone type must be home, work, or mobile';
    END IF;

    SELECT c.id INTO v_contact_id
    FROM contacts c
    WHERE c.name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" does not exist', p_contact_name;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, v_type)
    ON CONFLICT (contact_id, phone) DO UPDATE
    SET type = EXCLUDED.type;
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT g.id INTO v_group_id
    FROM groups g
    WHERE g.name = p_group_name;

    SELECT c.id INTO v_contact_id
    FROM contacts c
    WHERE c.name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" does not exist', p_contact_name;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    contact_id INTEGER,
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id AS contact_id,
        c.name AS contact_name,
        c.email,
        c.birthday,
        COALESCE(g.name, 'Other')::VARCHAR AS group_name,
        COALESCE(
            STRING_AGG(ph.type || ': ' || ph.phone, ', ' ORDER BY ph.id),
            ''
        )::TEXT AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE
        c.name ILIKE '%' || p_query || '%'
        OR COALESCE(c.email, '') ILIKE '%' || p_query || '%'
        OR COALESCE(g.name, '') ILIKE '%' || p_query || '%'
        OR EXISTS (
            SELECT 1
            FROM phones p2
            WHERE p2.contact_id = c.id
              AND p2.phone ILIKE '%' || p_query || '%'
        )
    GROUP BY c.id, c.name, c.email, c.birthday, g.name
    ORDER BY c.name;
END;
$$;


-- Practice 8-style pagination helper.
-- It is included here so the TSIS project can run on a fresh database.
CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INTEGER,
    p_offset INTEGER,
    p_sort_by TEXT DEFAULT 'name'
)
RETURNS TABLE(
    contact_id INTEGER,
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT,
    created_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id AS contact_id,
        c.name AS contact_name,
        c.email,
        c.birthday,
        COALESCE(g.name, 'Other')::VARCHAR AS group_name,
        COALESCE(
            STRING_AGG(ph.type || ': ' || ph.phone, ', ' ORDER BY ph.id),
            ''
        )::TEXT AS phones,
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
    ORDER BY
        CASE WHEN p_sort_by = 'name' THEN c.name END ASC,
        CASE WHEN p_sort_by = 'birthday' THEN c.birthday END ASC NULLS LAST,
        CASE WHEN p_sort_by = 'created_at' THEN c.created_at END ASC,
        c.id ASC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;
