# NUCC Ancestor Importer Project
===================

This is the output of the nucc_slurp repository

Data Source Summary
---------------------

The NUCC Ancestor Data file represents the second part of the NUCC provider taxonomy dataset. While the primary NUCC taxonomy file lists provider types and codes, the ancestor file defines the parent-child relationships between them—crucial for reconstructing the taxonomy hierarchy.

Unlike the main taxonomy file, which uses alphanumeric codes (e.g., 207L00000X), this file operates on numeric identifiers assigned to each taxonomy node. These numeric IDs are extracted from the NUCC website because not all intermediate branches in the taxonomy tree are assigned taxonomy codes—some internal nodes exist only as named groupings without associated codes. Thus, the numeric ID is the only reliable way to reconstruct the full tree structure.

We scrape these identifiers and relationships from the NUCC website to form a complete hierarchical model of the taxonomy, which cannot be built from the CSV files alone. This enriched structure is critical for applications that need to reason about provider specialties in a tree-like fashion.

Data Source Details
-------------------

* Schema Target: nucc_raw
* Table Target: nucc_ancestor
* Download URL:
* Create Table Statement:
