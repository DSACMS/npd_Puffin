# Puffin ETL Importers

## [CEHRT FHIR Endpoints Importer Project](./CEHRT_FHIR_endpoints)

The CHERT FHIR Endpoints are the result of the ehr_fhir_npi_slurp repo, which documents how to create these CSV files

### Data Source Summary

### Data Source Details

* Schema Target: lantern_ehr_fhir_raw
* Table Target: ehr_fhir_url
* Download URL: 
* Create Table Statement: [clean_npi_to_org_fhir_url.create_table_postgres.sql](./CEHRT_FHIR_endpoints/clean_npi_to_org_fhir_url.create_table_postgres.sql)


## [AHRQ CHSP Compendium Importer Project](./ahrq_chsp_compendium)

AHRQ Files are sourced from https://www.ahrq.gov/chsp/data-resources/compendium-2023.html

### Data Source Summary

### Data Source Details

* Schema Target: ahrq_chsp_raw
* Table Target: compendium
* Download URL https://www.ahrq.gov/chsp/data-resources/compendium-2023.html
* Create Table Statement: [chsp-compendium-2023.create_table_postgres.sql](./ahrq_chsp_compendium/chsp-compendium-2023.create_table_postgres.sql)


## [AHRQ CHSP Linkage Importer Project](./ahrq_chsp_linage)

AHRQ Files are sourced from https://www.ahrq.gov/chsp/data-resources/compendium-2023.html

### Data Source Summary

### Data Source Details

* Schema Target: ahrq_chsp_raw
* Table Target: compendium_linkage
* Download URL https://www.ahrq.gov/chsp/data-resources/compendium-2023.html
* Create Table Statement: [chsp-hospital-linkage-2023.create_table_postgres.sql](./ahrq_chsp_linage/chsp-hospital-linkage-2023.create_table_postgres.sql)


## [HHA All Owners Importer Project](./hha_all_owners)

There are several PECOS ownership files that are found here: https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy

### Data Source Summary

### Data Source Details

* Schema Target: pecos_raw
* Table Target: hha_all_owners
* Download URL https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy
* Create Table Statement: [HHA_All_Owners_2025.07.01.create_table_postgres.sql](./hha_all_owners/HHA_All_Owners_2025.07.01.create_table_postgres.sql)


## [Hospice All Owners Importer Project](./hospice_all_owners)

There are several PECOS ownership files that are found here: https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy

### Data Source Summary

### Data Source Details

* Schema Target: pecos_raw
* Table Target: hospice_all_owners
* Download URL https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy
* Create Table Statement: [Hospice_All_Owners_2025.07.01.create_table_postgres.sql](./hospice_all_owners/Hospice_All_Owners_2025.07.01.create_table_postgres.sql)


## [Hospital All Owners Importer Project](./hospital_all_owners)

There are several PECOS ownership files that are found here: https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy

### Data Source Summary

### Data Source Details

* Schema Target: pecos_raw
* Table Target: hospital_all_owners
* Download URL https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy
* Create Table Statement: [Hospital_All_Owners_2025.07.01.create_table_postgres.sql](./hospital_all_owners/Hospital_All_Owners_2025.07.01.create_table_postgres.sql)


## [NPPES Endpoint Importer Project](./nppes_endpoint)

Download the NPPES files from https://download.cms.gov/nppes/NPI_Files.html download the V2 version

### Data Source Summary

### Data Source Details

* Schema Target: nppes_raw
* Table Target: endpoint_file
* Download URL https://download.cms.gov/nppes/NPI_Files.html
* Create Table Statement: [endpoint_pfile_20050523-20250608.create_table_postgres.sql](./nppes_endpoint/endpoint_pfile_20050523-20250608.create_table_postgres.sql)


## [NPPES Main Importer Project](./nppes_main)

Download the NPPES files from https://download.cms.gov/nppes/NPI_Files.html download the V2 version

### Data Source Summary

### Data Source Details

* Schema Target: nppes_raw
* Table Target: main_file
* Download URL https://download.cms.gov/nppes/NPI_Files.html
* Create Table Statement: [npidata_pfile_20050523-20250608.create_table_postgres.sql](./nppes_main/npidata_pfile_20050523-20250608.create_table_postgres.sql)


## [NPPES Othername Importer Project](./nppes_othername)

Download the NPPES files from https://download.cms.gov/nppes/NPI_Files.html download the V2 version

### Data Source Summary

### Data Source Details

* Schema Target: nppes_raw
* Table Target: othername_file
* Download URL https://download.cms.gov/nppes/NPI_Files.html
* Create Table Statement: [othername_pfile_20050523-20250608.create_table_postgres.sql](./nppes_othername/othername_pfile_20050523-20250608.create_table_postgres.sql)


## [NPPES PL Importer Project](./nppes_pl)

Download the NPPES files from https://download.cms.gov/nppes/NPI_Files.html download the V2 version

### Data Source Summary

### Data Source Details

* Schema Target: nppes_raw
* Table Target: pl_file
* Download URL https://download.cms.gov/nppes/NPI_Files.html
* Create Table Statement: [pl_pfile_20050523-20250608.create_table_postgres.sql](./nppes_pl/pl_pfile_20050523-20250608.create_table_postgres.sql)


## [NUCC Importer Project](./nucc)

This is the output of the nucc_slurp repository

### Data Source Summary

### Data Source Details

* Schema Target: nucc_raw
* Table Target: nucc_merged_file
* Download URL: 
* Create Table Statement: [merged_nucc_data.create_table_postgres.sql](./nucc/merged_nucc_data.create_table_postgres.sql)


## [NUCC Ancestor Importer Project](./nucc_ancestor)

This is the output of the nucc_slurp repository

### Data Source Summary

### Data Source Details

* Schema Target: nucc_raw
* Table Target: nucc_ancestor
* Download URL: 
* Create Table Statement:


## [NUCC Sources Importer Project](./nucc_sources)

This is the output of the nucc_slurp repository

### Data Source Summary

### Data Source Details

* Schema Target: nucc_raw
* Table Target: nucc_sources
* Download URL: 
* Create Table Statement:


## [PECOS Assignment Importer Project](./pecos_assignment)

The PECOS Enrollment and Assignment data is downloaded here https://data.cms.gov/provider-characteristics/medicare-provider-supplier-enrollment/medicare-fee-for-service-public-provider-enrollment

### Data Source Summary

### Data Source Details

* Schema Target: pecos_raw
* Table Target: pecos_reassignment
* Download URL: https://data.cms.gov/provider-characteristics/medicare-provider-supplier-enrollment/medicare-fee-for-service-public-provider-enrollment
* Create Table Statement:


## [PECOS Enrollment Importer Project](./pecos_enrollment)

The PECOS Enrollment and Assignment data is downloaded here https://data.cms.gov/provider-characteristics/medicare-provider-supplier-enrollment/medicare-fee-for-service-public-provider-enrollment

### Data Source Summary

### Data Source Details

* Schema Target: pecos_raw
* Table Target: pecos_enrollment
* Download URL: https://data.cms.gov/provider-characteristics/medicare-provider-supplier-enrollment/medicare-fee-for-service-public-provider-enrollment
* Create Table Statement:


## [PECOS Ownership Importer Project](./pecos_ownership)

There are several PECOS ownership files that are found here: https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy

### Data Source Summary

### Data Source Details

* Schema Target: pecos_raw
* Table Target: hha_all_owners, hospice_all_owners, hospital_all_owners, rhc_all_owners, snf_all_owners
* Download URL: https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy
* Create Table Statement:


## [RHC All Owners Importer Project](./rhc_all_owners)

There are several PECOS ownership files that are found here: https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy

### Data Source Summary

### Data Source Details

* Schema Target: pecos_raw
* Table Target: rhc_all_owners
* Download URL: https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy
* Create Table Statement:


## [SNF All Owners Importer Project](./snf_all_owners)

There are several PECOS ownership files that are found here: https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy

### Data Source Summary

### Data Source Details

* Schema Target: pecos_raw
* Table Target: snf_all_owners
* Download URL: https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy
* Create Table Statement:


