# NPPES Othername Importer Project
===================

Download the NPPES files from https://download.cms.gov/nppes/NPI_Files.html download the V2 version

Data Source Summary
---------------------

The NPPES Other Name file is the simplest of the supplemental NPPES datasets. It contains only three columns:
	•	NPI
	•	OtherOrganizationName
	•	OtherOrganizationNameType

This file exclusively applies to organizational NPIs (Type 2) and does not include any information about individual providers (Type 1). It captures alternate names that an organization may operate under, such as “doing business as” (DBA) names, previous names, or other known aliases, with a corresponding type classification. Its minimal structure and focused scope make it straightforward to work with compared to other NPPES files.
Data Source Details

-------------------

* Schema Target: nppes_raw
* Table Target: othername_file
* Download URL https://download.cms.gov/nppes/NPI_Files.html
* Create Table Statement: [othername_pfile_20050523-20250608.create_table_postgres.sql](./othername_pfile_20050523-20250608.create_table_postgres.sql)
