import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv("data_file_locations.env")

required_vars = [
# TODO get from AHRQ section of data_file_locations.env
]

missing = [v for v in required_vars if os.getenv(v) is None]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

# Build commands
cmds = [
# TODO look in compile_cehrt_endpoints.py for example, all three steps need to be built for each of:
# local_data/ahrq_chsp_compendium/chsp-compendium-2023.csv
# local_data/ahrq_chsp_compendium/chsp-hospital-linkage-2023.csv
]

for cmd in cmds:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
