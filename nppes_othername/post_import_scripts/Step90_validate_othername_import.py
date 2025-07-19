#!/usr/bin/env python3
"""

The SQL 
SELECT
    provider_other_organization_name_type_code,
    COUNT(*) AS row_count,
    COUNT(DISTINCT(npi)) AS cnt_npi,
    COUNT(DISTINCT(provider_other_organization_name)) AS cnt_name
FROM nppes_raw.othername_file
GROUP BY provider_other_organization_name_type_code

Results in 
3,581770,564968,456029
4,32667,32024,27752
5,73911,72292,66378

these three provider_other_organization_name_type_code codes should have the same ratio of rows in the data over time. Make sure that they are within 10% of the percentages of the total rows they are now. 
Also there should be three and only three of these provider_other_organization_name_type_code codes.

The SQL 

SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT(npi)) AS cnt_npi,
    COUNT(DISTINCT(provider_other_organization_name)) AS cnt_name
FROM nppes_raw.othername_file

results in:

688348,660631,543487

There should be three and only three. 




"""

import os
from plainerflow import CredentialFinder, DBTable, InLaw  # type: ignore

def main():
    """
    Runs the validation tests for the NPPES othername data.
    """
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)

    print("Running validation tests for nppes_raw.othername_file...")
    InLaw.run_all(engine=alchemy_engine)

# Define tables once to be used by all tests
othername_DBTable = DBTable(schema='nppes_raw', table='othername_file')
main_DBTable = DBTable(schema='nppes_raw', table='main_file')

class ValidateRowCount(InLaw):
    """
    Validates that the othername_file table has at least one row.
    """
    title = "Table should have at least one row"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(*) as row_count FROM {othername_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="row_count",
            min_value=1
        )
        if result.success:
            return True
        return f"Row count validation failed: {result.result}"

class ValidateNpisAreInMain(InLaw):
    """
    Validates that all NPIs in the othername_file exist in the main_file.
    A left join from othername_file to main_file should not produce any nulls.
    """
    title = "All NPIs in othername_file must exist in main_file"

    @staticmethod
    def run(engine):
        sql = f"""
        SELECT COUNT(other.npi) AS missing_npi_count
        FROM {othername_DBTable} AS other
        LEFT JOIN {main_DBTable} AS main ON other.npi = main.npi
        WHERE main.npi IS NULL
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="missing_npi_count",
            min_value=0,
            max_value=0
        )
        if result.success:
            return True
        return f"Found NPIs in othername_file that are not in main_file: {result.result}"

class ValidateNpisAreOrganizations(InLaw):
    """
    Validates that all NPIs in the othername_file are Type 2 (Organizational) NPIs.
    The entity_type_code in the main_file should be 2 for all NPIs.
    """
    title = "All NPIs in othername_file must be organizational (Type 2)"

    @staticmethod
    def run(engine):
        sql = f"""
        SELECT COUNT(main.npi) AS non_organizational_npi_count
        FROM {main_DBTable} AS main
        JOIN {othername_DBTable} AS other ON main.npi = other.npi
        WHERE main.entity_type_code != '2'
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="non_organizational_npi_count",
            min_value=0,
            max_value=0
        )
        if result.success:
            return True
        return f"Found non-organizational NPIs in othername_file: {result.result}"

class ValidateOtherNameIsDifferentFromLegalName(InLaw):
    """
    Validates that the 'other name' is different from the legal business name.
    The purpose of the othername_file is to provide alternative names, not duplicates
    of the legal name found in the main_file.
    """
    title = "Other name should not be the same as the legal business name"

    @staticmethod
    def run(engine):
        sql = f"""
        SELECT
            COUNT(*) as same_name_count
        FROM {othername_DBTable} AS other
        JOIN {main_DBTable} AS main ON other.npi = main.npi
        WHERE other.provider_other_organization_name = main.provider_organization_name_legal_business_name
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="same_name_count",
            min_value=0,
            max_value=0
        )
        if result.success:
            return True
        return f"Found other names that are identical to the legal business name: {result.result}"

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        raise
