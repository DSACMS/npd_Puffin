Create Importer Readme.md
==================

The following sub-folders are NOT ETL projects. 

* AI_Instruction
* docs
* export
* import
* local_data
* sample_querys
* sql
* test_data_files
* test_invoker_data
* venv

All of the other sub-directories in the project correspond to a ETL project managed by csviper. You must read ../csviper/ReadMe.md to understand how csviper works.

Also, when you look inside a csviper directory, you see a go.postgresql.py script that csviper has generated.

For each of these projects, I would like to create a seperate ReadMe.md.
Much of the data in the ./data_file_locations.env file. Read this file now so that you understand its contents.

The ReadMe.md file should be added to the project sub-directory folder. So the nppes_main readme file will be ./nppes_main/ReadMe.md etc.

For a given ReadMe.md please prepopulate the following template as best you can. Treat the rest of this markdown file, as the template.

{REPLACE_ME} Importer Project
===================

{REPLACE_ME with the any comments from the relevant section of the data_file_locations.env file}

Data Source Summary
---------------------

{LEAVE THIS BLANK - it will be manually filled in by the user.}


Data Source Details
-------------------

* Schema Target: {REPLACE_ME with the schema name the data is imported into}
* Table Target: {REPLACE_ME with the table name that the data is imported into}
* Download URL {REPLACE_ME with the url documented in the data_file_locations.env }
* Create Table Statement: {REPLACE_ME with the link to the postgresql version of the create table statement}
