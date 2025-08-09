#!/usr/bin/env python3
"""
This script tests our basic expectations for what the othername file looks like.
It validates record counts and ensures that all NPIs in the othername file
are organizational NPIs that exist in the main NPI file.

It also validates the distribution of `provider_other_organization_name_type_code`
to ensure it remains consistent over time.
"""

import os
from npd_plainerflow import CredentialFinder, DBTable, InLaw  # type: ignore
from sqlalchemy import text

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

class ValidateJoinsToMainFile(InLaw):
    """
    Runs a suite of validation tests that depend on joining to the main_file.
    It first checks if the main_file is present and valid before running the tests.
    """
    title = "Suite of tests joining to the main_file"

    @staticmethod
    def run(engine):
        # 1. Pre-flight checks for main_file table
        with engine.connect() as connection:
            table_exists_sql = text("SELECT to_regclass('nppes_raw.main_file')")
            if not connection.execute(table_exists_sql).scalar():
                return "SKIPPED: The 'nppes_raw.main_file' table does not exist."

            row_count_sql = text("SELECT COUNT(*) FROM nppes_raw.main_file")
            row_count = connection.execute(row_count_sql).scalar()
            if row_count <= 1000000:
                return f"SKIPPED: The 'nppes_raw.main_file' has only {row_count} rows. Needs > 1,000,000."

            npi_type_sql = text("""
                SELECT data_type FROM information_schema.columns
                WHERE table_schema = 'nppes_raw' AND table_name = 'main_file' AND column_name = 'npi'
            """)
            npi_type = connection.execute(npi_type_sql).scalar()
            if npi_type and npi_type.lower() != 'bigint':
                return f"SKIPPED: The 'npi' column in 'nppes_raw.main_file' is '{npi_type}', not BIGINT."

        # 2. If pre-flight checks pass, run the dependent tests
        failures = []

        # Test 1: All NPIs in othername_file must exist in main_file
        sql1 = f"""
            SELECT COUNT(other.npi) AS missing_npi_count
            FROM {othername_DBTable} AS other
            LEFT JOIN {main_DBTable} AS main ON other.npi::BIGINT = main.npi
            WHERE main.npi IS NULL
        """
        gx_df1 = InLaw.to_gx_dataframe(sql1, engine)
        result1 = gx_df1.expect_column_values_to_be_between("missing_npi_count", 0, 0)
        if not result1.success:
            failures.append(f"Found NPIs in othername_file that are not in main_file: {result1.result}")

        # Test 2: All NPIs must be organizational
        sql2 = f"""
            SELECT COUNT(main.npi) AS non_organizational_npi_count
            FROM {main_DBTable} AS main
            JOIN {othername_DBTable} AS other ON main.npi = other.npi::BIGINT
            WHERE main.entity_type_code != '2'
        """
        gx_df2 = InLaw.to_gx_dataframe(sql2, engine)
        result2 = gx_df2.expect_column_values_to_be_between("non_organizational_npi_count", 0, 0)
        if not result2.success:
            failures.append(f"Found non-organizational NPIs in othername_file: {result2.result}")

        # Test 3: Other name should not be the same as legal name
        sql3 = f"""
            SELECT COUNT(*) as same_name_count
            FROM {othername_DBTable} AS other
            JOIN {main_DBTable} AS main ON other.npi::BIGINT = main.npi
            WHERE other.provider_other_organization_name = main.provider_organization_name_legal_business_name
        """
        gx_df3 = InLaw.to_gx_dataframe(sql3, engine)
        result3 = gx_df3.expect_column_values_to_be_between("same_name_count", 0, 0)
        if not result3.success:
            failures.append(f"Found other names that are identical to the legal business name: {result3.result}")

        if not failures:
            return True
        return "; ".join(failures)


class ValidateTypeCodeCount(InLaw):
    """
    Validates that there are exactly 3 distinct provider_other_organization_name_type_code values.
    This is based on the expectation that the source data consistently uses codes 3, 4, and 5.
    """
    title = "There should be exactly 3 distinct name type codes"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(DISTINCT provider_other_organization_name_type_code) as type_code_count FROM {othername_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="type_code_count",
            min_value=3,
            max_value=3
        )
        if result.success:
            return True
        return f"Expected 3 distinct type codes, but found a different number: {result.result}"


class ValidateTypeCodeRatios(InLaw):
    """
    Validates the distribution of rows for each name type code (3, 4, 5).
    The percentage of total rows for each code should be within a 10% relative tolerance
    of the historical baseline to detect significant shifts in data distribution.

    Baseline from 2025-07-19:
    - Code '3': 581,770 rows (~84.52%)
    - Code '4': 32,667 rows (~4.75%)
    - Code '5': 73,911 rows (~10.74%)
    - Total: 688,348 rows
    """
    title = "Row distribution for name type codes should be stable"

    @staticmethod
    def run(engine):
        sql = f"""
        WITH total_counts AS (
            SELECT CAST(COUNT(*) AS REAL) as total_rows FROM {othername_DBTable}
        ),
        type_code_counts AS (
            SELECT
                provider_other_organization_name_type_code,
                CAST(COUNT(*) AS REAL) as count_for_type
            FROM {othername_DBTable}
            GROUP BY provider_other_organization_name_type_code
        )
        SELECT
            tcc.provider_other_organization_name_type_code,
            tcc.count_for_type / tc.total_rows AS percentage
        FROM type_code_counts tcc, total_counts tc
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)

        # Validate ratios for each type code
        # Note: expect_column_values_to_be_in_set can't check ranges per value,
        # so we check each one with a filter. This is less efficient but more precise.

        # Code 3: ~84.52% -> Range [0.7607, 0.9297]
        result_3 = gx_df.expect_column_values_to_be_between(
            column="percentage",
            min_value=0.7607,
            max_value=0.9297,
            row_condition='provider_other_organization_name_type_code == "3"',
            condition_parser="pandas"
        )

        # Code 4: ~4.75% -> Range [0.04275, 0.05225]
        result_4 = gx_df.expect_column_values_to_be_between(
            column="percentage",
            min_value=0.04275,
            max_value=0.05225,
            row_condition='provider_other_organization_name_type_code == "4"',
            condition_parser="pandas"
        )

        # Code 5: ~10.74% -> Range [0.09666, 0.11814]
        result_5 = gx_df.expect_column_values_to_be_between(
            column="percentage",
            min_value=0.09666,
            max_value=0.11814,
            row_condition='provider_other_organization_name_type_code == "5"',
            condition_parser="pandas"
        )

        if result_3.success and result_4.success and result_5.success:
            return True

        failures = []
        if not result_3.success:
            failures.append(f"Type code '3' ratio out of range: {result_3.result}")
        if not result_4.success:
            failures.append(f"Type code '4' ratio out of range: {result_4.result}")
        if not result_5.success:
            failures.append(f"Type code '5' ratio out of range: {result_5.result}")

        return "; ".join(failures)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        raise
