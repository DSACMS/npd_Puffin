# CEHRT FHIR Endpoints Importer Project
===================

The CHERT FHIR Endpoints are the result of the ehr_fhir_npi_slurp repo, which documents how to create these CSV files

Data Source Summary
---------------------

The Lantern dataset is a public-use file derived from certified EHR vendor APIs that expose FHIR endpoint data, as required under the 21st Century Cures Act. Maintained by the Assistant Secretary for Technology Policy (formerly the ONC) Lantern’s core purpose is to test the technical conformity and availability of public FHIR endpoints associated with Electronic Health Record (EHR) systems. Each certified EHR vendor must publish a FHIR bulk data endpoint listing their customers’ individual endpoints, along with corresponding organizational NPIs.

Although Lantern itself is not the canonical source of this data, it offers a convenient and regularly updated snapshot in downloadable CSV format. This raw file enables downstream projects to easily integrate and test endpoint reachability and standards compliance. In this project, we use a separate scraper to parse and extract FHIR endpoint records from Lantern’s publication, storing them as CSV files for ingestion into the NDH data warehouse.

[The Lantern code is available on github.](https://github.com/onc-healthit/lantern-back-end)

Data Source Details
-------------------

* Schema Target: lantern_ehr_fhir_raw
* Table Target: ehr_fhir_url
* Download URL: REPLACE ME WITH NEW DSAC EHR SLURP URL
* Create Table Statement: [clean_npi_to_org_fhir_url.create_table_postgres.sql](./clean_npi_to_org_fhir_url.create_table_postgres.sql)
