#!/bin/bash
# Run all Step*.py scripts in order in this directory

set -e  # Exit immediately if a command exits with a non-zero status

cd "$(dirname "$0")"

for script in Step*.py; do
    if [[ -f "$script" ]]; then
        echo "Running $script"
        python3 "$script"
    fi
done
