import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("data_file_locations.env")

# Define a list of tuples, where each tuple contains the environment variables for a given file.
file_configs = [
    ("PECOS_OWNERSHIP_HHA_CSV_PATH", "pecos_ownership_raw", "hha_all_owners"),
    ("PECOS_OWNERSHIP_HOSPICE_CSV_PATH", "pecos_ownership_raw", "hospice_all_owners"),
    ("PECOS_OWNERSHIP_HOSPITAL_CSV_PATH", "pecos_ownership_raw", "hospital_all_owners"),
    ("PECOS_OWNERSHIP_RHC_CSV_PATH", "pecos_ownership_raw", "rhc_all_owners"),
    ("PECOS_OWNERSHIP_SNF_CSV_PATH", "pecos_ownership_raw", "snf_all_owners"),
]

# Dynamically build the command list
cmds = []
for csv_path_var, schema, table in file_configs:
    csv_path = os.getenv(csv_path_var)
    if not csv_path:
        print(f"Missing required environment variable: {csv_path_var}")
        sys.exit(1)

    output_dir = f"./{table}"
    metadata_path = os.path.join(output_dir, f"{os.path.basename(csv_path).replace('.csv', '')}.metadata.json")

    cmds.extend([
        [
            "csviper", "extract-metadata",
            f"--from_csv={csv_path}",
            f"--output_dir={output_dir}"
        ],
        [
            "csviper", "build-sql",
            f"--from_metadata_json={metadata_path}",
            f"--output_dir={output_dir}"
        ],
        [
            "csviper", "build-import-script",
            f"--from_resource_dir={output_dir}",
            f"--output_dir={output_dir}",
            "--overwrite_previous"
        ]
    ])

# Execute all commands
for cmd in cmds:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
