#!/usr/bin/env python3
"""
Fixes the npi as varchar import
"""

import plainerflow
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle, InLaw
import pandas as pd
import sqlalchemy
from pathlib import Path
import os

def main():

    is_just_print = False
    
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location) # grab the parents parents .env
    


    #npi_table = 'main_file_small' # For testing
    npi_table = 'main_file' # for production

    npi_DBTable = DBTable(schema='nppes_raw', table=npi_table)

    sql = FrostDict()

    sql['drop the new_npi column if exists from previous run'] = f"""
ALTER TABLE {npi_DBTable}
DROP COLUMN IF EXISTS new_NPI;
"""


    sql['create new_npi column'] = f"""
ALTER TABLE {npi_DBTable}
ADD COLUMN new_NPI BIGINT;        
    """

    sql['populate the bigint version from the varchar version'] = f"""
UPDATE {npi_DBTable}
SET new_NPI = "NPI"::BIGINT;
""" 
 
    sql['drop the varchar column'] = f"""
ALTER TABLE {npi_DBTable}
DROP COLUMN "NPI";
"""

    sql['rename new column'] = f"""
ALTER TABLE {npi_DBTable}
RENAME COLUMN new_NPI TO "NPI";
"""
    
    sql['drop the new_npi column if exists from previous run'] = f"""
ALTER TABLE {npi_DBTable}
DROP COLUMN IF EXISTS new_Replacement_NPI;
"""


    sql['create new_npi replacement column'] = f"""
ALTER TABLE {npi_DBTable}
ADD COLUMN new_Replacement_NPI BIGINT DEFAULT NULL;        
    """

    sql['populate the bigint version from the varchar version  replacement '] = f"""
UPDATE {npi_DBTable}
SET new_Replacement_NPI = NULLIF("Replacement_NPI", '')::BIGINT
""" 
 
    sql['drop the varchar  replacement column'] = f"""
ALTER TABLE {npi_DBTable}
DROP COLUMN "Replacement_NPI";
"""

    sql['rename new  replacement  column'] = f"""
ALTER TABLE {npi_DBTable}
RENAME COLUMN "new_Replacement_NPI" TO "Replacement_NPI";
"""

    # TODO 


    print("About to run SQL")
    SQLoopcicle.run_sql_loop(   sql_dict=sql,
                                is_just_print=is_just_print,
                                engine=alchemy_engine
    )
    

    class ValidateTotalSpentIsPositive(InLaw):
        title = "Active customers with orders should have positive total_spent"
        
        @staticmethod
        def run(alchemy_engine):
            sql = f"""
            SELECT COUNT(*) as invalid_count 
            FROM {npi_DBTable} 
            """
            validation_gx_df = InLaw.sql_to_gx_df(sql=sql, engine=alchemy_engine)
            
            invalid_count = validation_gx_df.iloc[0]['invalid_count']
            
            if invalid_count == 0:
                return True
            return f"Found {invalid_count} customers with orders but non-positive spending"
    

    #test_results = InLaw.run_all(engine=engine)
    


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install plainerflow pandas great-expectations")
        raise
        
