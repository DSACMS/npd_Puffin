# Hospital All Owners Importer Project
===================

There are several PECOS ownership files that are found here: https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy

Data Source Summary
---------------------
The PECOS All Owners dataset is a recently released, publicly available resource derived from the CMS Provider Enrollment, Chain, and Ownership System (PECOS). It comprises multiple files, each corresponding to a healthcare facility type—such as hospitals, clinics, skilled nursing facilities, home health agencies, rural health clinics, hospice, and federally qualified health centers. Of these, the hospital and clinic ownership files are the most crucial for our purposes, as they reveal associations between organizational NPIs that are effectively part of the same corporate entity.

Central to this dataset is the concept of the PAC ID (PECOS Associate Control ID), a 10-digit identifier that groups entities at the tax identification number (TIN) level. The PAC ID acts as a precursor to our internal “V10” model and may represent either organizations or individuals. Relationships between owning and owned entities are recorded as links between PAC IDs, with metadata such as ownership roles and percentage stakes sometimes included.

Additionally, the dataset includes Enrollment IDs, which describe the specific billing relationships each PAC ID holds with Medicare. While more complex joins across enrollment and ownership data may be necessary in other PECOS-derived datasets, the All Owners files themselves are relatively straightforward—primarily documenting direct ownership relationships.

This dataset enables us to enrich our organizational models by identifying when two or more organizational NPIs functionally belong to the same system or ownership group, which is essential for accurate healthcare system mapping and for supporting use cases like plan-participation modeling and endpoint federation.

Data Source Details
-------------------

* Schema Target: pecos_raw
* Table Target: hospital_all_owners
* Download URL https://data.cms.gov/search?keywords=All%20Owners&sort=Relevancy
* Create Table Statement: [Hospital_All_Owners_2025.07.01.create_table_postgres.sql](./Hospital_All_Owners_2025.07.01.create_table_postgres.sql)
