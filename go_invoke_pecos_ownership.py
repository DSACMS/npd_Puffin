import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("data_file_locations.env")

required_vars = [
    "PECOS_OWNERSHIP_IMPORT_DATA_DIR",
    "PECOS_DB_TYPE",
    "PECOS_SCHEMA",
    "PECOS_OWNERSHIP_HHA_TABLE",
    "PECOS_OWNERSHIP_HOSPICE_TABLE",
    "PECOS_OWNERSHIP_HOSPITAL_TABLE",
    "PECOS_OWNERSHIP_RHC_TABLE",
    "PECOS_OWNERSHIP_SNF_TABLE"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

table_vars = [
    "PECOS_OWNERSHIP_HHA_TABLE",
    "PECOS_OWNERSHIP_HOSPICE_TABLE",
    "PECOS_OWNERSHIP_HOSPITAL_TABLE",
    "PECOS_OWNERSHIP_RHC_TABLE",
    "PECOS_OWNERSHIP_SNF_TABLE"
]

cmds = []
for table_var in table_vars:
    table_name = os.getenv(table_var)
    output_dir = f"./{table_name}"
    cmds.append([
        "python", "-m", "csviper", "invoke-compiled-script",
        f"--run_import_from={output_dir}",
        f"--import_data_from_dir={os.getenv('PECOS_OWNERSHIP_IMPORT_DATA_DIR')}",
        f"--database_type={os.getenv('PECOS_DB_TYPE')}",
        f"--db_schema_name={os.getenv('PECOS_SCHEMA')}",
        f"--table_name={table_name}",
        "--trample"
    ])

for cmd in cmds:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
