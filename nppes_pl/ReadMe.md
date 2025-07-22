# NPPES PL Importer Project
===================

Download the NPPES files from https://download.cms.gov/nppes/NPI_Files.html download the V2 version

Data Source Summary
---------------------

The NPPES Practice Location file lists additional practice locations for providers beyond the primary address required in the main NPPES file. Introduced more recently, this file benefits from improved data quality due to NPPES’s adoption of U.S. Postal Service APIs for address validation. As a result, the address data in this file tends to be cleaner and more reliable. However, it only includes providers—individuals or organizations—who have opted to register multiple practice locations, so it does not represent a complete view of all provider addresses.

Data Source Details
-------------------

* Schema Target: nppes_raw
* Table Target: pl_file
* Download URL https://download.cms.gov/nppes/NPI_Files.html
* Create Table Statement: [pl_pfile_20050523-20250608.create_table_postgres.sql](./pl_pfile_20050523-20250608.create_table_postgres.sql)
