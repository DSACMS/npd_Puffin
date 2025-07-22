# NUCC Importer Project
===================

This is the output of the nucc_slurp repository

Data Source Summary
---------------------

The NUCC Provider Taxonomy is maintained by the National Uniform Claim Committee (NUCC) and provides standardized codes for classifying healthcare providers. The taxonomy is hierarchical and distinguishes between individual and organizational (non-individual) providers. However, the structure is inconsistent—subcategories like “groups of individuals” appear under the “individual” branch, leading to confusion.

Each taxonomy code is a string (e.g., 207L00000X for anesthesiology), and many specialties (such as addiction medicine) appear under multiple parent types (e.g., anesthesiology, psychiatry, pediatrics), without clear disambiguation. This reflects the training path rather than a coherent hierarchy—specialties appear under the branch where their prerequisite training lies.

Despite being hierarchical in concept, the taxonomy is not normalized: not all branches have their own codes, and a provider’s presence under a sub-branch doesn’t guarantee affiliation with its parent category. Furthermore, the taxonomy system is independent of the NPPES entity type system, so enforcement of organizational or individual classification is weak.

Data from NUCC comes in multiple forms:
	•	A free CSV file with basic codes and descriptions
	•	A paid CSV version with additional metadata
	•	The official NUCC website, which includes the parent-child structure not present in the CSV files

Because the free CSV lacks hierarchy metadata, we merge data scraped from the website with the CSV in a separate repository. That combined dataset is used to generate a cleaned CSV for import into Puffin.

Data Source Details
-------------------

* Schema Target: nucc_raw
* Table Target: nucc_merged_file
* Download URL: 
* Create Table Statement: [merged_nucc_data.create_table_postgres.sql](./merged_nucc_data.create_table_postgres.sql)
