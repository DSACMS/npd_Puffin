#!/usr/bin/env python3
"""
Drop old unique constraint on npi_id in ndh.organizational_npi if it exists.
"""

import os
from plainerflow import CredentialFinder
from sqlalchemy import text

def main():
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)

    with engine.begin() as conn:
        # Find the name of the unique constraint on npi_id
        result = conn.execute(text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'organizational_npi'
              AND table_schema = 'ndh'
              AND constraint_type = 'UNIQUE'
        """)).fetchall()
        for row in result:
            cname = row[0]
            # Check if this constraint is on npi_id only
            colres = conn.execute(text(f"""
                SELECT kcu.column_name
                FROM information_schema.key_column_usage kcu
                WHERE kcu.constraint_name = '{cname}'
                  AND kcu.table_name = 'organizational_npi'
                  AND kcu.table_schema = 'ndh'
                ORDER BY kcu.ordinal_position
            """)).fetchall()
            columns = [c[0] for c in colres]
            if columns == ['npi_id']:
                print(f"Dropping unique constraint {cname} on npi_id...")
                conn.execute(text(f'ALTER TABLE ndh.organizational_npi DROP CONSTRAINT {cname};'))
            else:
                print(f"Constraint {cname} is on columns {columns}, not dropping.")

    print("Old unique constraint on npi_id dropped if it existed.")

if __name__ == "__main__":
    main()
