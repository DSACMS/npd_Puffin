#!/bin/bash
#python -m csviper invoke-compiled-script --run_import_from=./nppes_main/ --import_data_from_dir=/Users/ftrotter/nppes_data/ --database_type=postgresql
python -m csviper invoke-compiled-script --run_import_from=./nppes_pl/ --import_data_from_dir=/Users/ftrotter/nppes_data/ --database_type=postgresql
python -m csviper invoke-compiled-script --run_import_from=./nppes_endpoint/ --import_data_from_dir=/Users/ftrotter/nppes_data/ --database_type=postgresql
python -m csviper invoke-compiled-script --run_import_from=./nppes_othername/ --import_data_from_dir=/Users/ftrotter/nppes_data/ --database_type=postgresql
