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

Please read docs/nppes/NPPES_ReadMe_And_CodeValues.md to understand the overall structure of the NPPES files.
Confirm that the fields that I have exposed in the sql/create_table_sql/create_npi.sql core NDH tables are in fact the only ones connected one-to-one with the NPI, or with a personal NPI or with an organizational NPI.

Unlike the Organizations, please go ahead and populate the links to Individuals (look in sql/create_table_sql/create_individual.sql) for more.
For now, ignore the Individuals credentials. Do not import them at all. A later ETL will address this. Do not import the Provider_Credential_Text at all.

We do not have the email or SSN for the individuals in the NPI database for now. Please leave these fields NULL.

FYI, despite documentation to the contrary the "NPI" column in nppes_raw.main_file is a BIGINT. Similarly all of the dates have been converted to postgresql DATE fields.
Please inspect nppes_main/post_import_scripts/Step05_fix_column_types.py to see how this was accomplished. 

In order to calculate if an organizational NPI has a parent organizational NPI, you must search all of the organizational NPI records to see if therre is one and only one organizational NPI that has the value
in its Provider_Organization_Name_Legal_Business_Name as an organization that lists itself as a subpart in the "Is_Organization_Subpart" field as yes..
in its "Parent_Organization_LBN". Please remove special characters and spaces, and only consider letters and numbers after converting all letters to lowercase for this comparision. 

There is a database table called intake.wrongnpi (look in sql/create_table_sql/create_intake_wrongnpi.sql) that can be used to mark failures in the processing.

When a organizational subpart NPI does not have a parent with the same legal business name, or there are more than one non-subpart organizational NPIs with the same legal business name...
This should be logged in wrongnpi.

You should create Records in the Individual table for Authorized Officials. For now, every distinct individual record should get a new record in the database. 
This is wrong, but we will not be correcting it for some time. Do not try and deduplicate authorized officials, or try to link in Individuals that are aquired from the individual NPI records. 

Please add a field mapping to this document before you begin coding a solution.