import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("data_file_locations.env")

required_vars = [
    "NPPES_MAIN_CSV",
    "NPPES_MAIN_DIR",
    "NPPES_MAIN_METADATA"
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

cmds = [
    [
        "csviper", "extract-metadata",
        f"--from_csv={os.getenv('NPPES_MAIN_CSV')}",
        f"--output_dir={os.getenv('NPPES_MAIN_DIR')}"
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
    ]
]

for cmd in cmds:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
