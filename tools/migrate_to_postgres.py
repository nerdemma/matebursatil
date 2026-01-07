"""Small script to migrate `data/cotizaciones.json` into Postgres.

Usage:
  DATABASE_URL=postgresql://user:pass@localhost:5432/db python tools/migrate_to_postgres.py
or
  python tools/migrate_to_postgres.py --db postgresql://user:pass@.. 
"""
import os
import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', help='Database URL (overrides DATABASE_URL env var)')
    parser.add_argument('--file', default='data/cotizaciones.json', help='Path to JSON file')
    args = parser.parse_args()

    db_url = args.db or os.getenv('DATABASE_URL')
    if not db_url:
        raise RuntimeError('DATABASE_URL not provided (env or --db)')

    with open(args.file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # import lazily to avoid requiring SQLAlchemy for non-migration runs
    from services.db import PostgresStorage

    storage = PostgresStorage(db_url)
    storage.write_all(data)
    print(f'Migrated {len(data)} items into Postgres')


if __name__ == '__main__':
    main()
