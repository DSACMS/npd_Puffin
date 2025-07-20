import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("data_file_locations.env")

def get_env_var(var_name: str) -> str:
    """Gets an environment variable or exits if it's not set."""
    value = os.getenv(var_name)
    if value is None:
        print(f"Error: Missing required environment variable: {var_name}", file=sys.stderr)
        sys.exit(1)
    return value

def main():
    """Main function to invoke AHRQ data import."""
    # Get required environment variables
    ahrq_comp_dir = get_env_var("AHRQ_COMP_DIR")
    ahrq_comp_import_data_dir = get_env_var("AHRQ_COMP_IMPORT_DATA_DIR")
    ahrq_comp_db_type = get_env_var("AHRQ_COMP_DB_TYPE")
    ahrq_comp_schema = get_env_var("AHRQ_COMP_SCHEMA")
    ahrq_comp_table = get_env_var("AHRQ_COMP_TABLE")
    
    ahrq_link_dir = get_env_var("AHRQ_LINK_DIR")
    ahrq_link_table = get_env_var("AHRQ_LINK_TABLE")

    cmds = [
        [
            "python", "-m", "csviper", "invoke-compiled-script",
            f"--run_import_from={ahrq_comp_dir}",
            f"--import_data_from_dir={ahrq_comp_import_data_dir}",
            f"--database_type={ahrq_comp_db_type}",
            f"--db_schema_name={ahrq_comp_schema}",
            f"--table_name={ahrq_comp_table}",
            "--trample"
        ],
        [
            "python", "-m", "csviper", "invoke-compiled-script",
            f"--run_import_from={ahrq_link_dir}",
            f"--import_data_from_dir={ahrq_comp_import_data_dir}",
            f"--database_type={ahrq_comp_db_type}",
            f"--db_schema_name={ahrq_comp_schema}",
            f"--table_name={ahrq_link_table}",
            "--trample"
        ]
    ]

    for cmd in cmds:
        print("Running:", " ".join(cmd))
        subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
