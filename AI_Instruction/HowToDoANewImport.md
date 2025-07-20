New Import Instructions
=====================

Follow these steps for each new data import:

The user will

* provide the directory where the csv files to import live.

Then you should:

* Create a new subdirectory for the import scripts on the main branch. Each file that needs to be imported gets its own project subdirectory.
* Create configuration values in data_file_locations.env The other values there should illustrate how to work in that file
* Related files in the same ./local_data directory should go into the same {last_subdirectory_of_import_path}_raw schema. The table names should reflect the file names, but brief.
* Create a "compiler" script. Read compile_nucc.py for an example.
* Create an "invoker" script. Read go_invoke_nucc.py for an example.

It is likely that the user will come back and tweak the schema and table names, etc. So please do not run the import, but wait for the user
to make those adjustments and the specificaly instruct the script to be run.
