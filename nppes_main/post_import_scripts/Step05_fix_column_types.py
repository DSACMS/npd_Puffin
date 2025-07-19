#!/usr/bin/env python3
"""
Fixes the npi as varchar import
"""

import plainerflow  # type: ignore
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle, InLaw # type: ignore
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

# Convert all of the NPI fields from VARCHAR to BIGINT. 

    sql['drop the new_npi column if exists from previous run'] = f"""
ALTER TABLE {npi_DBTable}
DROP COLUMN IF EXISTS new_npi;
"""

    sql['create new_npi column'] = f"""
ALTER TABLE {npi_DBTable}
ADD COLUMN new_npi BIGINT;        
    """

    sql['populate the bigint version from the varchar version'] = f"""
UPDATE {npi_DBTable}
SET new_npi = "npi"::BIGINT;
""" 
 
    sql['drop the varchar column'] = f"""
ALTER TABLE {npi_DBTable}
DROP COLUMN "npi";
"""

    sql['rename new column'] = f"""
ALTER TABLE {npi_DBTable}
RENAME COLUMN new_npi TO "npi";
"""
    

# Convert the Replacement NPI columns in a similar fashion

    sql['drop the new_npi replacement column if exists from previous run'] = f"""
ALTER TABLE {npi_DBTable}
DROP COLUMN IF EXISTS "new_replacement_npi";
"""


    sql['create new_npi replacement column'] = f"""
ALTER TABLE {npi_DBTable}
ADD COLUMN "new_replacement_npi" BIGINT DEFAULT NULL;        
    """

    sql['populate the bigint version from the varchar version  replacement '] = f"""
UPDATE {npi_DBTable}
SET "new_replacement_npi" = NULLIF("replacement_npi", '')::BIGINT
""" 
 
    sql['drop the varchar  replacement column'] = f"""
ALTER TABLE {npi_DBTable}
DROP COLUMN "replacement_npi";
"""

    sql['rename new  replacement  column'] = f"""
ALTER TABLE {npi_DBTable}
RENAME COLUMN "new_replacement_npi" TO "replacement_npi";
"""


    date_convertion_list = [
            'provider_enumeration_date'
            ,'last_update_date'
            ,'npi_deactivation_date'
            ,'npi_reactivation_date'
            ,'certification_date'
            ]

#TODO we should see if the database already has these as dates and only run the following loop for columns that are still text. 
# That will ensure that this script is idempotent


    for this_date_col in date_convertion_list:
        sql[f"Adding new col for {this_date_col}"] = f"""
ALTER TABLE {npi_DBTable}
ADD COLUMN "{this_date_col}_real_date" DATE DEFAULT NULL;
"""

        sql[f"convert string to date for {this_date_col}"] =f"""
UPDATE {npi_DBTable}
SET "{this_date_col}_real_date" = to_date(NULLIF("{this_date_col}", ''), 'MM/DD/YYYY');
"""
        
        sql[f"drop varchar for {this_date_col}"] = f"""ALTER TABLE {npi_DBTable} DROP COLUMN "{this_date_col}"; """

        sql[f"rename new col back to {this_date_col}"] = f"""ALTER TABLE {npi_DBTable} RENAME COLUMN "{this_date_col}_real_date" TO "{this_date_col}";"""

 
# TODO Lets make a new InLaw to check that all retired NPIs are in fact entirely blank in the data. Something like:
# SELECT * FROM nppes_raw.main_file WHERE "entity_type_code" = '' AND
#                                        ("provider_organization_name_legal_business_name" != '' OR "provider_last_name_legal_name" != '')
# is a start... but really it should check for every column except for the npi_deactivation_date and possible npi_deactivation_reason_code
# This code should go in nppes_main/post_import_scripts/Step90_validate_main_import.py


# TODO there should be an IF EXISTS for the index adding. 
    # Add unique key on NPI column to improve performance
    sql['add unique key on NPI column'] = f"""
ALTER TABLE {npi_DBTable}
ADD CONSTRAINT unique_npi_key UNIQUE ("npi");
"""

    sql['add index on npi and entity_type_code'] = f"""
CREATE INDEX IF NOT EXISTS idx_{npi_table}_npi_entity_type_code
ON {npi_DBTable}("npi", "entity_type_code");
"""

    print("About to run SQL")
    SQLoopcicle.run_sql_loop(   sql_dict=sql,
                                is_just_print=is_just_print,
                                engine=alchemy_engine
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install plainerflow pandas great-expectations")
        raise
