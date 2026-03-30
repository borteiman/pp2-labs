ALTER TABLE phonebook
ADD COLUMN IF NOT EXISTS surname VARCHAR(100);

UPDATE phonebook
SET surname = ''
WHERE surname IS NULL;