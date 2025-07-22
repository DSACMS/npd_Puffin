# NUCC Sources Importer Project
===================

This is the output of the nucc_slurp repository

Data Source Summary
---------------------

The NUCC Sources dataset is derived by scraping the notes section of the NUCC provider taxonomy website. While the downloadable CSV file lacks this information, the NUCC website often includes textual references to authoritative governing bodies—such as the American Board of Pediatrics or the American Board of Internal Medicine—that oversee particular taxonomy types.

Because these references are embedded informally within the notes field, we extract them using regex-based parsing, producing a structured dataset that links taxonomy codes to their associated certifying organizations. In some cases, multiple sources may be listed for a single taxonomy type.

Although syntactically inconsistent, this extracted data offers long-term potential for use in credential verification workflows, such as mapping provider specialties to legitimate board certifications and supporting ground truth validation of provider types.

Data Source Details
-------------------

* Schema Target: nucc_raw
* Table Target: nucc_sources
* Download URL: 
* Create Table Statement:
