# NPPES Endpoint Importer Project
===================

Download the NPPES files from https://download.cms.gov/nppes/NPI_Files.html download the V2 version

Data Source Summary
---------------------
The NPPES Endpoint file is a relatively recent addition to the NPPES data suite, released after years of delay despite its early prioritization by the interoperability community. This file provides structured metadata about electronic endpoints associated with healthcare organizations and providers, intended to support interoperability through FHIR and other standards.

Each row includes:
	•	Endpoint type and description
	•	The actual endpoint address (e.g., a URL or URI)
	•	Legal business name of the affiliated organization
	•	Intended use and use description, with an “other use” field for nonstandard purposes
	•	Content type and content description
	•	Associated location/address, typically identifying the organization’s address—even when endpoints are cloud-hosted and physically decoupled from that address

Despite its intended importance, this dataset is notoriously unreliable. It includes unvalidated and inconsistent entries such as personal email addresses and outdated or misconfigured URLs. Data quality is a major concern, and the lack of automated or manual validation by CMS makes this file challenging to use without additional cleaning.
Data Source Details
-------------------

* Schema Target: nppes_raw
* Table Target: endpoint_file
* Download URL https://download.cms.gov/nppes/NPI_Files.html
* Create Table Statement: [endpoint_pfile_20050523-20250608.create_table_postgres.sql](./endpoint_pfile_20050523-20250608.create_table_postgres.sql)
