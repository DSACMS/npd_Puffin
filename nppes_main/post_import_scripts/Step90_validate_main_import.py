#!/usr/bin/env python3
"""
This script validates the main NPPES data import.
"""

import os
import plainerflow  # type: ignore
from plainerflow import CredentialFinder, DBTable, InLaw
import sqlalchemy

class ValidateRetiredNPIsAreBlank(InLaw):
    """
    Checks that all retired NPIs are in fact entirely blank in the data,
    except for the npi_deactivation_date and npi_deactivation_reason_code.
    """
    title = "Retired NPIs should be blank"

    @staticmethod
    def run(engine):
        npi_DBTable = DBTable(schema='nppes_raw', table='main_file')
        
        # Get all column names from the table
        inspector = sqlalchemy.inspect(engine)
        columns = inspector.get_columns(npi_DBTable.table, schema=npi_DBTable.schema)
        column_names = [c['name'] for c in columns]
        
        # Columns to exclude from the check
        excluded_columns = [
            'npi',
            'entity_type_code',
            'npi_deactivation_reason_code',
            'npi_deactivation_date',
            'npi_reactivation_date'
        ]
        
        # Build the query to check for non-blank values in other columns
        conditions = []
        column_types = {c['name']: str(c['type']) for c in columns}
        for col in column_names:
            if col not in excluded_columns:
                col_type = column_types.get(col, '').upper()
                if 'CHAR' in col_type or 'TEXT' in col_type or 'VARCHAR' in col_type:
                    conditions.append(f"""("{col}" IS NOT NULL AND "{col}" != '')""")
                else:
                    conditions.append(f"""("{col}" IS NOT NULL)""")
        
        sql = f"""
        SELECT COUNT(*) as violation_count
        FROM {npi_DBTable}
        WHERE "entity_type_code" = '' AND ({' OR '.join(conditions)})
        """
        
        gx_df = InLaw.to_gx_dataframe(sql, engine)
        
        result = gx_df.expect_column_values_to_be_between(
            column="violation_count",
            min_value=0,
            max_value=0
        )
        
        if result.success:
            return True
        
        return f"Found non-blank values in retired NPI records: {result.result}"


def main():
    """
    Main function to run the validation tests.
    """
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)

    print("Running validation tests...")
    test_results = InLaw.run_all(engine=alchemy_engine)
    
    # You can add additional logic here to handle test results if needed
    print("Validation tests complete.")
    print(test_results)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install plainerflow pandas great-expectations")
        raise
