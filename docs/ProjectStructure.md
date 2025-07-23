# Project Structure and Data Pipeline

## Overview

This document outlines the architecture and data flow of the National Healthcare Directory (NDH) project. The primary goal of this project is to create a comprehensive, accurate, and up-to-date directory of healthcare providers and organizations in the United States. It achieves this by ingesting, transforming, and integrating data from various sources into a unified, normalized PostgreSQL database.

The final product is a database that allows users to query for healthcare providers (both individuals and organizations) and retrieve detailed information, including their contact details, specialties, and, most importantly, their associated FHIR interoperability endpoints.

## Core Concepts

The project revolves around several key concepts:

* **NPI (National Provider Identifier):** A unique 10-digit identification number issued to health care providers in the United States by the Centers for Medicare and Medicaid Services (CMS). NPIs are the central identifier used to link data across different sources.
* **Clinical Organization:** A legal entity that provides healthcare services. The project distinguishes between the legal entity and its various "doing business as" (DBA) or brand names.
* **Individual Provider:** A person who provides healthcare services, such as a doctor or nurse.
* **Interoperability Endpoint:** A URL that provides access to a provider's electronic health record (EHR) data via the FHIR (Fast Healthcare Interoperability Resources) standard. A primary goal of the project is to link NPIs to these endpoints.
* **Data Sources:** The project integrates data from several key sources, including:
* **NPPES (National Plan and Provider Enumeration System):** The primary source for NPI data.
* **PECOS (Provider Enrollment, Chain, and Ownership System):** Provides information about Medicare-enrolled providers and their relationships.
* **CEHRT (Certified EHR Technology):** Provides a list of certified EHR products and their FHIR endpoints.
* **AHRQ (Agency for Healthcare Research and Quality):** Provides data on hospitals and health systems.
* **NUCC (National Uniform Claim Committee):** Provides the Health Care Provider Taxonomy code set.

## Data Pipeline

The project uses a robust ETL (Extract, Transform, Load) pipeline to process data from the various sources. The pipeline can be broken down into the following stages:

1. **Configuration:** The `data_file_locations.env` file is the central configuration file for the ETL process. It defines the paths to the source CSV files and the target database schemas and tables for each data source.

2. **Extraction and Raw Import:** For each data source, a dedicated directory contains the scripts and configuration for that source.
    * A **"compiler" script** (e.g., `compile_nppes_main.py`) prepares the raw data for import, often by generating SQL `CREATE TABLE` and `COPY` statements from a template.
    * An **"invoker" script** (e.g., `go_invoke_nppes.py`) executes the import process, loading the raw CSV data into a corresponding table in the `nppes_raw` schema (or a similar raw schema for other data sources).

3. **Post-Import Transformation:** After the raw data is imported, a series of **post-import scripts** are executed. These scripts are located in the `post_import_scripts` subdirectory for each ETL. They perform a variety of transformations, including:
    * **Data Cleaning:** Fixing data types (e.g., converting NPIs from `VARCHAR` to `BIGINT`, converting strings to dates), handling missing values, and standardizing formats.
    * **Normalization:** Breaking down wide, denormalized source files into a set of smaller, well-structured tables in the `ndh` schema.
    * **Enrichment:** Creating new data elements, such as row hashes for change detection.
    * **Relationship Building:** Linking data across different tables and data sources.

4. **Validation:** The project uses the `InLaw` data validation framework (built on Great Expectations) to ensure data quality at various stages of the pipeline. Validation scripts (e.g., `Step90_validate_main_import.py`) check for expected record counts, data distributions, and referential integrity.

5. **Analysis:** After the data has been transformed and validated, analysis scripts (e.g., `Step25_analyze_npi_data.py`) are run to generate summary statistics and data quality metrics. The results of this analysis are stored in tables in the `analysis` schema.

## Database Schema

The project uses a PostgreSQL database with several schemas to organize the data:

* **`nppes_raw` (and other `*_raw` schemas):** These schemas contain the raw, unprocessed data as it was imported from the source CSV files. The table structures in these schemas closely mirror the structure of the source files.

* **`intake`:** This schema contains tables used for staging data and tracking changes during the ETL process. Key tables include:
* `staging_phone`: For normalizing phone numbers.
* `npi_processing_run`, `npi_change_log`, `individual_change_log`, `parent_relationship_change_log`: For tracking changes in the NPPES data over time.
* `wrongnpi`: For logging NPIs that are known to be incorrect.

* **`ndh` (National Directory of Healthcare):** This is the final, normalized schema that contains the clean, integrated data. It is the primary schema that end-users will query. Key tables include:
* `npi`, `individual_npi`, `organizational_npi`: The core tables for NPI data.
* `individual`, `clinical_organization`: For storing information about individual providers and organizations.
* `address`, `phone`: For storing normalized contact information.
* `interop_endpoint`: For storing FHIR endpoint URLs.
* `provider_taxonomy`: For storing NUCC and Medicare provider taxonomy information.
* `payer_data`: For storing information about insurance payers and plans.

* **`analysis`:** This schema contains tables that store the results of the data analysis and quality checks. These tables provide a high-level overview of the data and can be used to monitor the health of the data pipeline.

## ETL Processes

The project consists of several distinct ETL processes, one for each data source. Each ETL process follows the general data pipeline described above. The main ETLs are:

* **NPPES ETLs (`nppes_main`, `nppes_othername`, `nppes_pl`, `nppes_endpoint`):** These are the most complex ETLs in the project. They process the main NPPES data files, which are very large and denormalized, and transform them into the core `ndh` schema. The `nppes_main` ETL includes a sophisticated incremental update process to handle monthly data releases.
* **CEHRT FHIR Endpoints ETL (`CEHRT_FHIR_endpoints`):** This ETL imports a list of FHIR endpoints and links them to NPIs.
* **AHRQ ETLs (`ahrq_chsp_compendium`, `ahrq_chsp_linage`):** These ETLs import data about hospitals and health systems from the Agency for Healthcare Research and Quality.
* **PECOS ETLs (`pecos_assignment`, `pecos_enrollment`, `pecos_ownership`):** These ETLs import data about Medicare-enrolled providers and their ownership and assignment relationships.
* **NUCC ETLs (`nucc`, `nucc_ancestor`, `nucc_sources`):** These ETLs import the NUCC Health Care Provider Taxonomy data.

## Key Technologies

The project is built on a foundation of open-source technologies:

* **Python:** The primary language used for the ETL scripts.
* **PostgreSQL:** The relational database used to store the data.
* **`plainerflow`:** A custom Python library that provides a framework for building simple, SQL-based ETL pipelines. It includes components for database connection management (`CredentialFinder`), SQL execution (`SQLoopcicle`), and data validation (`InLaw`).
* **`pandas`:** Used for data manipulation in some of the ETL scripts.
* **`sqlalchemy`:** Used for interacting with the PostgreSQL database.
* **`great_expectations`:** The underlying library used by the `InLaw` framework for data validation.
