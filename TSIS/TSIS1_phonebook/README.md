# TSIS 1 PhoneBook — Extended Contact Management

## Create database

```bash
psql -U postgres -d postgres
```

```sql
CREATE DATABASE phonebook_tsis;
\q
```

## Edit database.ini

Put your real PostgreSQL password:

```ini
[postgresql]
host=localhost
database=phonebook_tsis
user=postgres
password=your_password
port=5432
```

## Install package

```bash
pip install psycopg2-binary
```

## Run

```bash
python phonebook.py
```

First choose:

```text
1. Setup database schema and procedures
```

## Features

- Extended schema: contacts, phones, groups
- Multiple phone numbers per contact
- Email and birthday fields
- Contact groups/categories
- Search by name, email, group and all phones
- Filter by group
- Sort by name, birthday, date added
- Paginated console navigation
- CSV import with new fields
- JSON export/import with duplicate handling
- Procedure add_phone
- Procedure move_to_group
- Function search_contacts
