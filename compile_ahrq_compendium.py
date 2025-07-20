import os
import sys
import subprocess
from dotenv import load_dotenv

def get_env_var(var_name: str) -> str:
    """Gets an environment variable or exits if it's not set."""
    value = os.getenv(var_name)
    if value is None:
        print(f"Error: Missing required environment variable: {var_name}", file=sys.stderr)
        sys.exit(1)
    return value

def main():
    """Main function to compile AHRQ data."""
    load_dotenv("data_file_locations.env")

    # Get required environment variables
    ahrq_comp_csv = get_env_var("AHRQ_COMP_CSV")
    ahrq_comp_dir = get_env_var("AHRQ_COMP_DIR")
    ahrq_link_csv = get_env_var("AHRQ_LINK_CSV")
    ahrq_link_dir = get_env_var("AHRQ_LINK_DIR")

    comp_metadata_path = os.path.join(ahrq_comp_dir, os.path.basename(ahrq_comp_csv).replace('.csv', '.metadata.json'))
    link_metadata_path = os.path.join(ahrq_link_dir, os.path.basename(ahrq_link_csv).replace('.csv', '.metadata.json'))

    # Build commands
    cmds = [
        [
            "csviper", "extract-metadata",
            f"--from_csv={ahrq_comp_csv}",
            f"--output_dir={ahrq_comp_dir}"
        ],
        [
            "csviper", "build-sql",
            f"--from_metadata_json={comp_metadata_path}",
            f"--output_dir={ahrq_comp_dir}",
            "--overwrite_previous"
        ],
        [
            "csviper", "build-import-script",
            f"--from_resource_dir={ahrq_comp_dir}",
            f"--output_dir={ahrq_comp_dir}",
            "--overwrite_previous"
        ],
        [
            "csviper", "extract-metadata",
            f"--from_csv={ahrq_link_csv}",
            f"--output_dir={ahrq_link_dir}"
        ],
        [
            "csviper", "build-sql",
            f"--from_metadata_json={link_metadata_path}",
            f"--output_dir={ahrq_link_dir}",
            "--overwrite_previous"
        ],
        [
            "csviper", "build-import-script",
            f"--from_resource_dir={ahrq_link_dir}",
            f"--output_dir={ahrq_link_dir}",
            "--overwrite_previous"
        ]
    ]

    for cmd in cmds:
        print("Running:", " ".join(cmd))
        subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
