#!/bin/bash
# individual scripts
#csviper extract-metadata --from_csv=/Users/ftrotter/Downloads/NPPES_Data_Dissemination_June_2025_V2/endpoint_pfile_20050523-20250608.csv --output_dir=./nppes_endpoint/ --overwrite_previous
#csviper build-sql --from_metadata_json=./nppes_endpoint/endpoint_pfile_20050523-20250608.metadata.json --output_dir=./nppes_endpoint/ --overwrite_previous
#csviper build-import-script --from_resource_dir=./nppes_endpoint/ --output_dir=./nppes_endpoint/ --overwrite_previous


csviper full-compile --from_csv=/Users/ftrotter/Downloads/NPPES_Data_Dissemination_June_2025_V2/endpoint_pfile_20050523-20250608.csv --output_dir=./nppes_endpoint/ --overwrite_previous
python ./nppes_endpoint/go.postgresql.py --csv_file=/Users/ftrotter/Downloads/NPPES_Data_Dissemination_June_2025_V2/endpoint_pfile_20050523-20250608.csv --db_schema_name=nppes_raw --table_name=endpoint_file
