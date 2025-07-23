#!/usr/bin/env python3
"""
This validates that basic counts in the additional address file are reasonable. 



"""

import os
import ndh_plainerflow  # type: ignore
from ndh_plainerflow import CredentialFinder, DBTable, InLaw # type: ignore

# Define the table
pl_DBTable = DBTable(schema='nppes_raw', table='pl_file')

class ValidateRowCount(InLaw):
    title = "Row count should be within 5% of 1,032,599"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(*) AS row_count FROM {pl_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        min_val = 1032599 * 0.95
        max_val = 1032599 * 1.05
        result = gx_df.expect_column_values_to_be_between(
            column="row_count",
            min_value=min_val,
            max_value=max_val
        )
        if result.success:
            return True
        return f"Row count validation failed: expected between {min_val} and {max_val}, but got {result.result['observed_value']}"

class ValidateNpiCount(InLaw):
    title = "Distinct NPI count should be within 5% of 693,207"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(DISTINCT npi) AS cnt_npi FROM {pl_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        min_val = 693207 * 0.95
        max_val = 693207 * 1.05
        result = gx_df.expect_column_values_to_be_between(
            column="cnt_npi",
            min_value=min_val,
            max_value=max_val
        )
        if result.success:
            return True
        return f"Distinct NPI count validation failed: expected between {min_val} and {max_val}, but got {result.result['observed_value']}"

class ValidatePostalCodeCount(InLaw):
    title = "Distinct postal code count should be within 5% of 339,107"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(DISTINCT provider_secondary_practice_address_postal_code) AS cnt_postal_code FROM {pl_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        min_val = 339107 * 0.95
        max_val = 339107 * 1.05
        result = gx_df.expect_column_values_to_be_between(
            column="cnt_postal_code",
            min_value=min_val,
            max_value=max_val
        )
        if result.success:
            return True
        return f"Distinct postal code count validation failed: expected between {min_val} and {max_val}, but got {result.result['observed_value']}"

class ValidateStateCodeCount(InLaw):
    title = "Distinct state code count should be within 5% of 290"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(DISTINCT provider_secondary_practice_address_state_name) AS cnt_state_code FROM {pl_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        min_val = 290 * 0.95
        max_val = 290 * 1.05
        result = gx_df.expect_column_values_to_be_between(
            column="cnt_state_code",
            min_value=min_val,
            max_value=max_val
        )
        if result.success:
            return True
        return f"Distinct state code count validation failed: expected between {min_val} and {max_val}, but got {result.result['observed_value']}"

class ValidateCountryCodeCount(InLaw):
    title = "Distinct country code count should be within 5% of 70"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(DISTINCT provider_secondary_practice_address_country_code) AS cnt_country_code FROM {pl_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        min_val = 70 * 0.95
        max_val = 70 * 1.05
        result = gx_df.expect_column_values_to_be_between(
            column="cnt_country_code",
            min_value=min_val,
            max_value=max_val
        )
        if result.success:
            return True
        return f"Distinct country code count validation failed: expected between {min_val} and {max_val}, but got {result.result['observed_value']}"


def main():
    """
    Main function to run the InLaw validation tests.
    """
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)

    print("Running validation tests...")
    InLaw.run_all(engine=alchemy_engine)
    print("Validation tests complete.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install ndh_plainerflow pandas great-expectations")
        raise
