#!/bin/bash
python -m csviper invoke-compiled-script --run_import_from=./nppes_pl/ --import_data_from_dir=/Users/ftrotter/nppes_data/ --database_type=postgresql --db_schema_name=nppes_raw --table_name=pl_file
python -m csviper invoke-compiled-script --run_import_from=./nppes_endpoint/ --import_data_from_dir=/Users/ftrotter/nppes_data/ --database_type=postgresql --db_schema_name=nppes_raw --table_name=endpoint_file
python -m csviper invoke-compiled-script --run_import_from=./nppes_othername/ --import_data_from_dir=/Users/ftrotter/nppes_data/ --database_type=postgresql --db_schema_name=nppes_raw --table_name=othername_file
python -m csviper invoke-compiled-script --run_import_from=./nppes_main/ --import_data_from_dir=/Users/ftrotter/nppes_data/ --database_type=postgresql --db_schema_name=nppes_raw --table_name=main_file
