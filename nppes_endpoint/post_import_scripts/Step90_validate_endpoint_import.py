#!/usr/bin/env python3
"""
This script tests our basic expectations for what the endpoint file looks like.
It validates record counts and ratios to ensure data quality and consistency.
"""

import os
from npd_plainerflow import CredentialFinder, DBTable, InLaw  # type: ignore

def main():
    """
    Runs the validation tests for the NPPES endpoint data.
    """
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)

    print("Running validation tests for nppes_raw.endpoint_file...")
    InLaw.run_all(engine=alchemy_engine)

# Define the table once to be used by all tests
endpoint_DBTable = DBTable(schema='nppes_raw', table='endpoint_file')

class ValidateNpiCount(InLaw):
    """
    Validates that the distinct NPI count is within 5% of the expected baseline.
    Expected: 476,736
    """
    title = "NPI count should be within 5% of expected value"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(DISTINCT npi) as value FROM {endpoint_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="value",
            min_value=452899,  # 476736 * 0.95
            max_value=500573   # 476736 * 1.05
        )
        if result.success:
            return True
        return f"NPI count validation failed: {result.result}"

class ValidateEndpointTypeCount(InLaw):
    """
    Validates that the distinct endpoint_type count is within 5% of the expected baseline.
    Expected: 6
    """
    title = "Endpoint type count should be within 5% of expected value"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(DISTINCT endpoint_type) as value FROM {endpoint_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="value",
            min_value=5,  # 6 * 0.95 rounded
            max_value=7   # 6 * 1.05 rounded
        )
        if result.success:
            return True
        return f"Endpoint type count validation failed: {result.result}"

class ValidateEndpointTypeDescriptionCount(InLaw):
    """
    Validates that the distinct endpoint_description count is within 5% of the expected baseline.
    Expected: 27,611
    """
    title = "Endpoint type description count should be within 5% of expected value"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(DISTINCT endpoint_description) as value FROM {endpoint_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="value",
            min_value=26230,  # 27611 * 0.95
            max_value=28992   # 27611 * 1.05
        )
        if result.success:
            return True
        return f"Endpoint type description count validation failed: {result.result}"

class ValidateEndpointCount(InLaw):
    """
    Validates that the distinct endpoint count is within 5% of the expected baseline.
    Expected: 342,583
    """
    title = "Endpoint count should be within 5% of expected value"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(DISTINCT endpoint) as value FROM {endpoint_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="value",
            min_value=325454,  # 342583 * 0.95
            max_value=359712   # 342583 * 1.05
        )
        if result.success:
            return True
        return f"Endpoint count validation failed: {result.result}"

class ValidatePostalCodeCount(InLaw):
    """
    Validates that the distinct postal code count is within 5% of the expected baseline.
    Expected: 149,132
    """
    title = "Postal code count should be within 5% of expected value"

    @staticmethod
    def run(engine):
        sql = f"SELECT COUNT(DISTINCT affiliation_address_postal_code) as value FROM {endpoint_DBTable}"
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="value",
            min_value=141675,  # 149132 * 0.95
            max_value=156589   # 149132 * 1.05
        )
        if result.success:
            return True
        return f"Postal code count validation failed: {result.result}"

class ValidateNpiToEndpointRatio(InLaw):
    """
    Validates that the ratio of distinct endpoints to distinct NPIs is between 50% and 90%.
    """
    title = "Ratio of endpoints to NPIs should be between 50% and 90%"

    @staticmethod
    def run(engine):
        sql = f"""
        SELECT
            CAST(COUNT(DISTINCT endpoint) AS REAL) / CAST(COUNT(DISTINCT npi) AS REAL) as ratio
        FROM {endpoint_DBTable}
        """
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        result = gx_df.expect_column_values_to_be_between(
            column="ratio",
            min_value=0.5,
            max_value=0.9
            
        )
        if result.success:
            return True
        return f"NPI to endpoint ratio validation failed: {result.result}"


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        raise
