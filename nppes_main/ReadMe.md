# NPPES Main Importer Project
===================

Download the NPPES files from https://download.cms.gov/nppes/NPI_Files.html download the V2 version

Data Source Summary
---------------------

The NPPES main file (National Plan and Provider Enumeration System) is the most structurally complex dataset in the NDH data ingestion pipeline. It represents a flat, unnormalized CSV file that includes detailed enumeration records for both individual and organizational healthcare providers. The key differentiator between these two provider types is the Entity Type Code, which allows the file to serve as a merged schema for two logically distinct record types.

For individuals, the file includes personal name components (first, last, middle, suffix, prefix, credentials) as well as “other last names” with type codes, which are frequently used for aliases such as maiden names. For organizations, the file provides a legal business name and typically one “other name,” often the DBA. Only organizations have a designated authorized official, whose name and credentials are included in the far-right columns of the file—added in a backward-compatible way over time.

Both individuals and organizations are assigned:
	•	Mailing and practice addresses
	•	Taxonomy codes and state licenses, encoded using NUCC taxonomy codes and repeated across multiple flat columns (e.g., Taxonomy_1, Taxonomy_2, etc.)
	•	Identifiers, such as state Medicaid or license numbers, organized per state. Though originally intended to consolidate identifiers across systems, this block is now less useful due to decreasing reliance on external IDs.
	•	Provider type metadata, such as “Is Sole Proprietor” and “Subpart” flags.

Sensitive fields such as Tax ID and Parent Organization Tax ID have been redacted in the public version, though Parent Organization Legal Name remains and can be used for limited relationship modeling.

The dataset design prioritizes wide, flat CSV compatibility over normalization, resulting in repetitive column structures that are difficult to parse. Despite its complexity and partial redaction, the NPPES main file remains the foundational source for enumerating U.S. healthcare providers.

There is a data documentation pdf that accompanies the download which contains most of this information and there is also a "codeset" pdf which has the various nppes codesets in the file (things like "other name type")

Data Source Details
-------------------

* Schema Target: nppes_raw
* Table Target: main_file
* Download URL https://download.cms.gov/nppes/NPI_Files.html
* Create Table Statement: [npidata_pfile_20050523-20250608.create_table_postgres.sql](./npidata_pfile_20050523-20250608.create_table_postgres.sql)
