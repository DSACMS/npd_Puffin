#!/usr/bin/env python3
"""
This is a CLI python script that reads in the contents of the parent .env 
And then exports all of the raw data import schemas into ./local_data/export/

Each schema should have its own pgdump command. 

read data_file_locations.env for a list of the schemas to be exported. Anything with "raw" in the name should be exported
Make a list of the things that are exported this way at the beginning of the program and then export each one seperately into {this_schema}.pg.sql

Export both the table structure and data
"""

import os
import subprocess
import time
from dotenv import load_dotenv

def get_raw_schemas(env_file):
    """
    Parses the given .env file and returns a list of schema names containing 'raw'.
    """
    schemas = []
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                if 'SCHEMA' in key and 'raw' in value:
                    schemas.append(value)
    return list(set(schemas)) # Return unique schemas

def main():
    """
    Main function to export raw schemas.
    """
    # Load database configuration from parent .env file
    parent_env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if not os.path.exists(parent_env_path):
        print(f"Error: Parent .env file not found at {parent_env_path}")
        return
        
    load_dotenv(dotenv_path=parent_env_path)

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    if not all([db_user, db_password, db_host, db_port, db_name]):
        print("Error: Database connection details not found in .env file.")
        print("Please ensure DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, and DB_NAME are set.")
        return

    # Find schemas to export
    data_locations_env = 'data_file_locations.env'
    if not os.path.exists(data_locations_env):
        print(f"Error: {data_locations_env} not found.")
        return
        
    schemas_to_export = get_raw_schemas(data_locations_env)
    
    if not schemas_to_export:
        print("No raw schemas found to export.")
        return

    print("The following raw schemas will be exported:")
    for schema in schemas_to_export:
        print(f"- {schema}")

    # Create export directory
    export_dir = './local_data/export/'
    os.makedirs(export_dir, exist_ok=True)
    print(f"\nExporting to directory: {export_dir}")

    # Set PGPASSWORD environment variable for pg_dump
    if db_password:
        os.environ['PGPASSWORD'] = db_password
    else:
        print("Error: DB_PASSWORD is not set.")
        return

    # Export each schema
    for schema in schemas_to_export:
        export_path = os.path.join(export_dir, f"{schema}.pg.sql")
        print(f"Exporting schema '{schema}' to '{export_path}'...")
        
        command = [
            'pg_dump',
            '--no-owner',
            '--schema', schema,
            '-U', db_user,
            '-h', db_host,
            '-p', db_port,
            db_name
        ]
        
        try:
            start_time = time.time()
            with open(export_path, 'w') as f:
                subprocess.run(command, stdout=f, check=True, text=True)
            end_time = time.time()
            duration = end_time - start_time
            print(f"Successfully exported schema '{schema}' in {duration:.2f} seconds.")
        except subprocess.CalledProcessError as e:
            print(f"Error exporting schema '{schema}': {e}")
        except FileNotFoundError:
            print("Error: 'pg_dump' command not found. Make sure PostgreSQL client tools are installed and in your PATH.")
            break

    # Unset PGPASSWORD
    if 'PGPASSWORD' in os.environ:
        del os.environ['PGPASSWORD']
    print("\nExport process complete.")

if __name__ == "__main__":
    main()
