# PECOS Assignment Importer Project
===================

The PECOS Enrollment and Assignment data is downloaded here https://data.cms.gov/provider-characteristics/medicare-provider-supplier-enrollment/medicare-fee-for-service-public-provider-enrollment

Data Source Summary
---------------------

The PECOS Assignment dataset records instances where an individual provider assigns their Medicare payments to another entity, such as a group practice, clinic, or health system. This is common in outpatient billing, where Medicare reimbursement is calculated at the individual provider level, but the actual payment is directed to an affiliated organization.

The dataset is critical for mapping individual NPIs to organizational PAC IDs that receive payment on their behalf, revealing real-world employment or affiliation structures in Medicare billing. It captures one of the two meanings of “assignment” in healthcare: the provider-to-organization payment assignment (as opposed to patient-to-provider benefit assignment). Understanding these assignments provides key insights into financial and operational relationships within provider networks.

Assignment is on a per-enrollment basis and has the be used with the original assignment file to reduce down to PAC to PAC associations, which represent the underlying relationships.

Data Source Details
-------------------

* Schema Target: pecos_raw
* Table Target: pecos_reassignment
* Download URL: https://data.cms.gov/provider-characteristics/medicare-provider-supplier-enrollment/medicare-fee-for-service-public-provider-enrollment
* Create Table Statement:
