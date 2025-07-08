#!/bin/bash
python -m csviper invoke-compiled-script --run_import_from=./CHERT_FHIR_endpoints/ --import_data_from_dir=/Users/ftrotter/gitgov/ftrotter/ehr_fhir_npi_slurp/data/output_data/ --database_type=postgresql --db_schema_name=lantern_ehr_fhir_raw --table_name=ehr_fhir_url
