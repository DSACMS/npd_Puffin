# PECOS Enrollment Importer Project
===================

The PECOS Enrollment and Assignment data is downloaded here https://data.cms.gov/provider-characteristics/medicare-provider-supplier-enrollment/medicare-fee-for-service-public-provider-enrollment

Data Source Summary
---------------------

The PECOS Enrollment dataset maps Medicare/Medicaid billing privileges—referred to as enrollments—to healthcare entities identified by PAC IDs. A PAC ID represents either an individual or organization and is tied to a Tax Identification Number (TIN). Each enrollment represents a specific approval to bill Medicare or Medicaid for a particular service type.

This file provides a one-to-many relationship between PAC IDs and enrollments, allowing insight into which entities are actively participating in government programs. It also includes demographic and organizational details such as legal business names, making it a valuable source for validating provider identity and organizational structure within the PECOS system.

Data Source Details
-------------------

* Schema Target: pecos_raw
* Table Target: pecos_enrollment
* Download URL: https://data.cms.gov/provider-characteristics/medicare-provider-supplier-enrollment/medicare-fee-for-service-public-provider-enrollment
* Create Table Statement:
