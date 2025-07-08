#!/bin/bash

# RUN ONE AT A TIME: 

csviper extract-metadata --from_csv=/Users/ftrotter/gitgov/ftrotter/ehr_fhir_npi_slurp/data/output_data/clean_npi_to_org_fhir_url.csv --output_dir=./CHERT_FHIR_endpoints/ 
csviper build-sql --from_metadata_json=./CHERT_FHIR_endpoints/clean_npi_to_org_fhir_url.metadata.json --output_dir=./CHERT_FHIR_endpoints/ --overwrite_previous
csviper build-import-script --from_resource_dir=./CHERT_FHIR_endpoints/ --output_dir=./CHERT_FHIR_endpoints/ --overwrite_previous

#RUN ALL AT ONCE
#csviper full-compile --from_csv=/Users/ftrotter/Downloads/NPPES_Data_Dissemination_June_2025_V2/endpoint_pfile_20050523-20250608.csv --output_dir=./CHERT_FHIR_endpoints/ 
