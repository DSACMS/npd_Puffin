How This All Works
==================

You MUST read all of the files that I reference before doing anything else.

This file should summarize how this set of ETLs arrives at a comprehensive National Healthcare Directory.

First, the file nppes_main/post_import_scripts/Step47_check_ehr_fhir_url.py contains the tests that need to pass for a working NDH.
Which should allow someone to search for a provider and get a matching FHIR endpoint, by JOINing across the databases.

Then read AI_Instruction/HowToDoANewImport.md which details how a single ETL project should be structured.

Then read data_file_locations.env which details the source CSV files and where they should endup in the postgresql database.

Then read every create table statement in ./sql/create_table_sql This will show you the structure of the whole project. 

Then look in every sub-directory in the ndh_Puffin main directory. If it has a go.postgresql.py file, then it is an ETL.

Read the Postgresql CREATE TABLE template sql file. The name will be different per ETL subdirectory, but it will look like this file: ppes_main/npidata_pfile_20050523-20250608.create_table_postgres.sql

Sometimes in these ETL sub-directory there will be a subdirectory called post_import_scripts. If this directory exists, read every file inside the directory.
These are the data transformation steps that build the ndh schema contents from the raw imports.

Then place your best understanding of how this project works in docs/ProjectStructure.md
