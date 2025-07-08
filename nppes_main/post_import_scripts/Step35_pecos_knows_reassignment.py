#!/usr/bin/env python3
"""
Step35_pecos_knows_reassignment.py

This script processes PECOS reassignment data to populate the ndh.assigning_npi table.
The reassignment data maps PECOS organizations that are assigning benefits to NPIs that are receiving them.

The process:
1. Drop and recreate the ndh.assigning_npi table
2. Map reassignment relationships from PECOS data to NDH structure
3. Use INNER JOINs to ensure underlying data exists in target tables

Data Flow:
- pecos_reassignment.reasgn_bnft_enrlmt_id -> ClinicalOrganization_id (via PECOS VTIN)
- pecos_reassignment.rcv_bnft_enrlmt_id -> npi_id (via pecos_enrollment.npi)
"""

import plainerflow  # type: ignore
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle  # type: ignore
import pandas as pd
import sqlalchemy
from pathlib import Path
import os

class Step35PecosKnowsReassignment:
    
    @staticmethod
    def main():
        is_just_print = False  # Start with dry-run mode
        
        print("Connecting to DB")
        base_path = os.path.dirname(os.path.abspath(__file__))
        env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
        alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)
        
        # Define table references using PlainerFlow DBTable pattern
        pecos_reassignment_DBTable = DBTable(schema='pecos_raw', table='pecos_reassignment')
        pecos_enrollment_DBTable = DBTable(schema='pecos_raw', table='pecos_enrollment')
        clinical_org_DBTable = DBTable(schema='ndh', table='ClinicalOrganization')
        assigning_npi_DBTable = DBTable(schema='ndh', table='assigning_npi')
        
        sql = FrostDict()
        
        # Phase 1: Drop and recreate the assigning_npi table
        sql['drop_assigning_npi_table'] = f"""
        DROP TABLE IF EXISTS {assigning_npi_DBTable};
        """
        
        sql['create_assigning_npi_table'] = f"""
        CREATE TABLE {assigning_npi_DBTable} (
            ClinicalOrganization_id INT NOT NULL,
            npi_id INT NOT NULL
        );
        """
        
        pecos_vtin_prefix = 'PECOS'

        # Phase 2: Populate the assigning_npi table with reassignment data
        sql['populate_assigning_npi'] = f"""
        INSERT INTO {assigning_npi_DBTable} (
            ClinicalOrganization_id,
            npi_id
        )
        SELECT 
            clinical_org.id AS ClinicalOrganization_id, 
            CAST(receiving_enrollment.npi AS INTEGER) AS npi_id
        FROM {pecos_reassignment_DBTable} AS reassignment
        INNER JOIN {pecos_enrollment_DBTable} AS assigning_enrollment ON
            reassignment.reasgn_bnft_enrlmt_id = assigning_enrollment.enrlmt_id
        INNER JOIN {pecos_enrollment_DBTable} AS receiving_enrollment ON
            reassignment.rcv_bnft_enrlmt_id = receiving_enrollment.enrlmt_id
        INNER JOIN {clinical_org_DBTable} AS clinical_org ON
            clinical_org.organization_vtin = CONCAT('{pecos_vtin_prefix}',receiving_enrollment.pecos_asct_cntl_id);
        """
        
        # Phase 3: Create indexes for performance
        sql['create_assigning_npi_org_index'] = f"""
        CREATE INDEX IF NOT EXISTS idx_assigning_npi_org_id 
        ON {assigning_npi_DBTable}(ClinicalOrganization_id);
        """
        
        sql['create_assigning_npi_npi_index'] = f"""
        CREATE INDEX IF NOT EXISTS idx_assigning_npi_npi_id 
        ON {assigning_npi_DBTable}(npi_id);
        """
        
        # Phase 4: Create compound index for unique lookups
        sql['create_assigning_npi_compound_index'] = f"""
        CREATE INDEX IF NOT EXISTS idx_assigning_npi_compound 
        ON {assigning_npi_DBTable}(ClinicalOrganization_id, npi_id);
        """
        
        print("About to run SQL")
        SQLoopcicle.run_sql_loop(
            sql_dict=sql,
            is_just_print=is_just_print,
            engine=alchemy_engine
        )
        
        print("✅ Successfully processed PECOS reassignment data into ndh.assigning_npi table")

def main():
    try:
        Step35PecosKnowsReassignment.main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install plainerflow pandas great-expectations")
        raise

if __name__ == "__main__":
    main()
