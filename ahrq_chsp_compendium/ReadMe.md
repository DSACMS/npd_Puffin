# AHRQ CHSP Compendium Importer Project
===================

AHRQ Files are sourced from https://www.ahrq.gov/chsp/data-resources/compendium-2023.html

Data Source Summary
---------------------

The AHRQ Compendium of U.S. Health Systems is maintained by the Agency for Healthcare Research and Quality ([AHRQ](https://www.ahrq.gov/)) and provides a curated list of healthcare systems in the United States. It describes affiliations between hospitals, group practices, outpatient sites, nursing homes, and home health agencies within larger health systems. The compendium is derived from a merger of two commercial datasets: the American Hospital Association ([AHA](https://www.aha.org/)) Annual Survey and IQVIA’s [OneKey](https://www.iqvia.com/solutions/commercialization/data-and-information-management/onekey) dataset, which together offer the most comprehensive view of health system structure currently available.

Although the data has a significant lag—typically updated annually and often released nearly two years later—it remains a valuable reference due to the relative stability of system affiliations. The compendium includes two main files: one describing systems and another describing their constituent hospitals, which are identified using CMS Certification Numbers (CCNs). While CCNs do not directly link to organizational NPIs or Tax Identification Numbers (TINs), a supplemental VRDC dataset is under development to map these relationships and enhance interoperability.

This dataset is the main file that lists the systems.

Data Source Details
-------------------

* Schema Target: ahrq_chsp_raw
* Table Target: compendium
* Download URL https://www.ahrq.gov/chsp/data-resources/compendium-2023.html
* Create Table Statement: [chsp-compendium-2023.create_table_postgres.sql](./chsp-compendium-2023.create_table_postgres.sql)
