Populating NDH NPI data
=========================

I would like to populate the three basic NPI tables in the ndh database found here sql/create_table_sql/create_npi.sql

The NPI record here: nppes_main/npidata_pfile_20050523-20250608.create_table_postgres.sql
is the datasource and it will be found under nppes_raw.main_file in the database. 

See AI_Instruction/PlainerflowTools.md for the basics of building out a simple ETL pipeline by putting plainerflow scripts in the post_import_scripts directory of nppes_main.


An NPI comes in two flavors, dependant on the contents of the Entity_Type_Code variable. A 1 for an entity type code means that the provider is an individual. A doctor, nurse or some other kind of individual practicioner. 
Every individual gets one and only one NPI. 

An organization can have as many type 2 NPI records as they like. Organizational NPI records can also have sub-parts, which means they link back to themselves. 
In the NDH model, we identify an organization has having one tax identifier, which we model as a VTIN, which is usually a hash of an EIN. 

Later, we will try and associate the VTINS with specific Organizational EINs. Which means that when we create a record in the ndh.NPI_to_ClinicalOrganization table for each organizational NPI, we will simply use the link to ClinicalOrganization_id as NULL.
A later ETL will address that association. 

