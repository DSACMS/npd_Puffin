#!/usr/bin/env python3
"""
This is a python program that accepts a CLI argument for the import sql dumps: (and defaults to ../local_data/export/)
This will loop over each of the .sql files found in that directory and use psql command.. powered by the .env contents to get passwords etc. 

To import the data into the exact same database.schema as the original dump file. 

Please read the ../.env file to use the right variables.
"""

import os
import subprocess
import time
import argparse
from dotenv import load_dotenv  # type: ignore

def main():
    """
    Main function to import SQL dumps.
    """
    parser = argparse.ArgumentParser(description="Import SQL dumps from a specified directory.")
    parser.add_argument(
        'import_dir', 
        nargs='?', 
        default='../local_data/export/', 
        help='Directory containing .pg.sql dump files. Defaults to ../local_data/export/'
    )
    args = parser.parse_args()

    import_dir = args.import_dir

    if not os.path.isdir(import_dir):
        print(f"Error: Import directory not found at {import_dir}")
        return

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

    # Find SQL files to import
    sql_files = [f for f in os.listdir(import_dir) if f.endswith('.pg.sql')]
    
    if not sql_files:
        print(f"No .pg.sql files found in {import_dir} to import.")
        return

    print("The following SQL dump files will be imported:")
    for sql_file in sql_files:
        print(f"- {sql_file}")

    # Set PGPASSWORD environment variable for psql
    if db_password:
        os.environ['PGPASSWORD'] = db_password
    else:
        print("Error: DB_PASSWORD is not set.")
        return

    # Import each SQL file
    for sql_file in sql_files:
        import_path = os.path.join(import_dir, sql_file)
        print(f"Importing file '{import_path}' into database '{db_name}'...")
        
        command = [
            'psql',
            '-U', db_user,
            '-h', db_host,
            '-p', db_port,
            '-d', db_name,
            '-f', import_path
        ]
        
        try:
            start_time = time.time()
            # Using subprocess.run to execute the command
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            end_time = time.time()
            duration = end_time - start_time
            print(f"Successfully imported '{sql_file}' in {duration:.2f} seconds.")
            if result.stdout:
                print("Output:\n", result.stdout)
            if result.stderr:
                print("Errors:\n", result.stderr)

        except subprocess.CalledProcessError as e:
            print(f"Error importing file '{sql_file}': {e}")
            print(f"Stderr: {e.stderr}")
            print(f"Stdout: {e.stdout}")
        except FileNotFoundError:
            print("Error: 'psql' command not found. Make sure PostgreSQL client tools are installed and in your PATH.")
            break

    # Unset PGPASSWORD
    if 'PGPASSWORD' in os.environ:
        del os.environ['PGPASSWORD']
    print("\nImport process complete.")

if __name__ == "__main__":
    main()
