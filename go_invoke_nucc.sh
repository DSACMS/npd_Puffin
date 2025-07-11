#!/bin/bash
python -m csviper invoke-compiled-script --run_import_from=./nucc/ --import_data_from_dir=../nucc_slurp/data/ --database_type=postgresql --db_schema_name=nucc_raw --table_name=nucc_merged_file
python -m csviper invoke-compiled-script --run_import_from=./nucc_sources/ --import_data_from_dir=../nucc_slurp/data/ --database_type=postgresql --db_schema_name=nucc_raw --table_name=nucc_sources
python -m csviper invoke-compiled-script --run_import_from=./nucc_ancestor/ --import_data_from_dir=../nucc_slurp/data/ --database_type=postgresql --db_schema_name=nucc_raw --table_name=nucc_ancestor
