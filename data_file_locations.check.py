#!/usr/bin/env python3
# This script loads the data_file_loations.env file and simply verifies that all of the csv files referenced there exist.
import os
from dotenv import dotenv_values

def main():
    """
    Reads the data_file_locations.env file, extracts file paths,
    and checks if the files exist.
    """
    env_file_path = 'data_file_locations.env'
    if not os.path.exists(env_file_path):
        print(f"Error: {env_file_path} not found.")
        return

    print(f"Checking file paths in {env_file_path}...")

    config = dotenv_values(env_file_path)
    all_files_found = True

    for key, value in config.items():
        if value and ('_CSV' in key or value.endswith('.csv')):
            # Expand user home directory if ~ is used
            expanded_value = os.path.expanduser(value)
            
            if not os.path.exists(expanded_value):
                print(f"  [MISSING] Not Found: {key}={expanded_value}")
                all_files_found = False

    if all_files_found:
        print("all good")

if __name__ == "__main__":
    main()
