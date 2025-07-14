import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("setup.env")

required_vars = [
    "NPPES_MAIN_CSV",
    "NPPES_MAIN_DIR",
    "NPPES_MAIN_METADATA",
    "NPPES_RAW_SCHEMA",
    "NPPES_MAIN_TABLE"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmds = [
    [
        "csviper", "extract-metadata",
        f"--from_csv={os.getenv('NPPES_MAIN_CSV')}",
        f"--output_dir={os.getenv('NPPES_MAIN_DIR')}",
        "--overwrite_previous"
    ],
    [
        "csviper", "build-sql",
        f"--from_metadata_json={os.getenv('NPPES_MAIN_METADATA')}",
        f"--output_dir={os.getenv('NPPES_MAIN_DIR')}",
        "--overwrite_previous"
    ],
    [
        "csviper", "build-import-script",
        f"--from_resource_dir={os.getenv('NPPES_MAIN_DIR')}",
        f"--output_dir={os.getenv('NPPES_MAIN_DIR')}",
        "--overwrite_previous"
    ],
    [
        "python", "./nppes_main/go.postgresql.py",
        f"--csv_file={os.getenv('NPPES_MAIN_CSV')}",
        f"--db_schema_name={os.getenv('NPPES_RAW_SCHEMA')}",
        f"--table_name={os.getenv('NPPES_MAIN_TABLE')}"
    ]
]

for cmd in cmds:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
