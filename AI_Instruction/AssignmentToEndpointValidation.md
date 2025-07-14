Validate NPI assignment and endpoint data
==================

I would like you to write a script that calls system to use the command-line grep command to grep for precisely, only, and exactly the NPIs that I tell you to look for. The NPIs are the 10 digit numbers that I am going to list shortly. You will look for them in the files that I sepecify will precisely and exactly tell you which files to look for them in. I do not want you to write a general script. I do not want you to write a database script. I want you to do only what I am asking you to do in this message. Do not write a program that searches other files. Do not write a program that searches using different NPIs.

Ignore the database testing instructions, because I am not asking you to test a database. I am asking you to test the contents of CSV files on the file system.

For the first part of the script, I would like you to make system calls using GREP on files in precise locations on the file system. Using this, we will look inside the origin CSV files to make sure that the data that we think is in those files is in those files in the format that we want to see. So the NPIs are:

* 1043699168 - Woodridge Primary Clinic
* 1023008976 - Dr Hussain

The files to check are:

* The pecos enrollment file at: /Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Enrollment_Extract_2025.04.01.csv
* The pecos reassignment file at: /Users/ftrotter/Downloads/Medicare_Fee-For-Service_Public_Provider_Enrollment/2025-Q1/PPEF_Reassignment_Extract_2025.04.01.csv
* The FHIR endpoint data at: /Users/ftrotter/gitgov/ftrotter/ehr_fhir_npi_slurp/data/output_data/clean_npi_to_org_fhir_url.csv

The file structure of the enrollment file is:
NPI,PECOS_ASCT_CNTL_ID,ENRLMT_ID,PROVIDER_TYPE_CD,PROVIDER_TYPE_DESC,STATE_CD,FIRST_NAME,MDL_NAME,LAST_NAME,ORG_NAME

Use the NPI of each provider to get the ENRLMT_ID of the provider.
Then when you search the pecos reassignment file, use the ENRLMT_ID instead of the NPI.

Finally when you search the FHIR endpint file you will again use the NPI.

What we expect:

* There should be two different rows for the two NPIs in the enrollment file
* There should be one identical row of data in the assignment file that shows the Dr. Hussien assigns payment to Woodridge, but via enrollment ids instead of NPIs
* There should be one row of data in the EHR file that matches the NPI of Woodridge

Place the the resulting code here: nppes_main/post_import_scripts/Step40_validate_assignment_to_endpoint.py
