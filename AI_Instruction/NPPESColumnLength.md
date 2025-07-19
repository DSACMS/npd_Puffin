NPPES column length fix
==============

The csviper system is capable of detecting the max length of a csv file column which works pretty well.

However in the case of NPPES, we know that they have specific limits on the length of columns that are supposed to be supported by each field.

Those character counts are listed in the documentation, which we have turned into a markdown file here: docs/nppes/NPPES_ReadMe_And_CodeValues.md

For the following files:

* nppes_endpoint/endpoint_pfile_20050523-20250608.metadata.json
* nppes_main/npidata_pfile_20050523-20250608.metadata.json
* nppes_othername/othername_pfile_20050523-20250608.metadata.json
* nppes_pl/pl_pfile_20050523-20250608.metadata.json

Please confirm the longer of the two values (the length inferred by csviper and the length in the documentation) is listed plus on character.
So when the current value in the metadata files is 99 and the documentation says 100, make it 101.
Generally, the documented values should be longer.

Please remember all of the cases where the actual data in the csv file (i.e. what is in the metadata.json file) is longer than what is in the documentation and at the end of the process, please write these in a list below in this file:

* Healthcare Provider Taxonomy Group_1
* Healthcare Provider Taxonomy Group_2
* Healthcare Provider Taxonomy Group_3
* Healthcare Provider Taxonomy Group_4
* Healthcare Provider Taxonomy Group_5
* Healthcare Provider Taxonomy Group_6
* Healthcare Provider Taxonomy Group_7
* Healthcare Provider Taxonomy Group_8
* Healthcare Provider Taxonomy Group_9
* Healthcare Provider Taxonomy Group_10
* Healthcare Provider Taxonomy Group_11
* Healthcare Provider Taxonomy Group_12
* Healthcare Provider Taxonomy Group_13
* Healthcare Provider Taxonomy Group_14
* Healthcare Provider Taxonomy Group_15
