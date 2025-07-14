#!/usr/bin/env python3
"""
Fix ndh.organizational_npi.id to be auto-incrementing (serial/identity).
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
        # 1. Create the sequence if it does not exist
        seq_exists = conn.execute(
            text("""
            SELECT 1 FROM information_schema.sequences
            WHERE sequence_name = 'organizational_npi_id_seq'
            AND sequence_schema = 'ndh'
            """)
        ).fetchone()
        if not seq_exists:
            print("Creating sequence ndh.organizational_npi_id_seq...")
            conn.execute(text("CREATE SEQUENCE ndh.organizational_npi_id_seq;"))
        else:
            print("Sequence already exists.")

        # 2. Set the default for the id column
        print("Setting default for ndh.organizational_npi.id...")
        conn.execute(text(
            "ALTER TABLE ndh.organizational_npi "
            "ALTER COLUMN id SET DEFAULT nextval('ndh.organizational_npi_id_seq');"
        ))

    print("Auto-increment default set for ndh.organizational_npi.id.")

if __name__ == "__main__":
    main()
