#!/bin/bash

# RUN ONE AT A TIME: 

# Nucc nodes
csviper extract-metadata --from_csv=../nucc_slurp/data/merged_nucc_data.csv --output_dir=./nucc/ 
csviper build-sql --from_metadata_json=./nucc/merged_nucc_data.metadata.json --output_dir=./nucc/ 
csviper build-import-script --from_resource_dir=./nucc/ --output_dir=./nucc/ --overwrite_previous

# Nucc ancestors
csviper extract-metadata --from_csv=../nucc_slurp/data/nucc_parent_code.csv --output_dir=./nucc_ancestor/ 
csviper build-sql --from_metadata_json=./nucc_ancestor/nucc_parent_code.metadata.json --output_dir=./nucc_ancestor/ 
csviper build-import-script --from_resource_dir=./nucc_ancestor/ --output_dir=./nucc_ancestor/ --overwrite_previous


# Nucc sources
csviper extract-metadata --from_csv=../nucc_slurp/data/nucc_sources.csv --output_dir=./nucc_sources/ 
csviper build-sql --from_metadata_json=./nucc_sources/nucc_sources.metadata.json --output_dir=./nucc_sources/ 
csviper build-import-script --from_resource_dir=./nucc_sources/ --output_dir=./nucc_sources/ --overwrite_previous
