#!/usr/bin/env python3
"""
Core NPI Pipeline: Incremental Update of NDH NPI tables from NPPES raw data

This script implements the Core NPI Pipeline with incremental update support for monthly NPPES releases.
It populates three main NDH tables:
1. ndh.NPI - Core NPI records for both individual and organizational providers
2. ndh.individual_npi - Links individual NPIs to Individual records
3. ndh.organizational_npi - Links organizational NPIs to Clinical Organizations

Key Features:
- Incremental updates: Only processes changed/new NPIs
- Change tracking: Logs all changes to intake tables
- Data preservation: Maintains existing data, only updates what changed
- Monthly processing: Designed for monthly NPPES file releases
- Simple SQL: No CTEs, uses intermediate tables for clarity

Processing phases broken into small, clear steps following DRY principles.
"""

import npd_plainerflow  # type: ignore
from npd_plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle  # type: ignore
import os

def main():
    # Control dry-run mode - start with True to preview SQL
    is_just_print = False
    
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)
    
    # Define source and target tables
    #npi_table = 'main_file_small'  # For testing
    npi_table = 'main_file'  # For production
    source_DBTable = DBTable(schema='nppes_raw', table=npi_table)
    
    # Target NDH tables
    npi_DBTable = DBTable(schema='ndh', table='npi')
    individual_DBTable = DBTable(schema='ndh', table='individual')
    npi_to_individual_DBTable = DBTable(schema='ndh', table='individual_npi')
    npi_to_clinical_org_DBTable = DBTable(schema='ndh', table='organizational_npi')
    wrongnpi_DBTable = DBTable(schema='intake', table='wrongnpi')
    
    # Intake tracking tables
    processing_run_DBTable = DBTable(schema='intake', table='npi_processing_run')
    npi_change_log_DBTable = DBTable(schema='intake', table='npi_change_log')
    individual_change_log_DBTable = DBTable(schema='intake', table='individual_change_log')
    parent_change_log_DBTable = DBTable(schema='intake', table='parent_relationship_change_log')
    
    # Intermediate working tables (regular tables in intake schema, cleaned up each run)
    current_run_DBTable = DBTable(schema='intake', table='temp_current_run')
    npi_changes_DBTable = DBTable(schema='intake', table='temp_npi_changes')
    individual_provider_changes_DBTable = DBTable(schema='intake', table='temp_individual_provider_changes')
    authorized_official_changes_DBTable = DBTable(schema='intake', table='temp_authorized_official_changes')
    normalized_org_names_DBTable = DBTable(schema='intake', table='temp_normalized_org_names')
    parent_matches_DBTable = DBTable(schema='intake', table='temp_parent_matches')
    resolved_parents_DBTable = DBTable(schema='intake', table='temp_resolved_parents')
    parent_changes_DBTable = DBTable(schema='intake', table='temp_parent_changes')
    multi_parent_npis_DBTable = DBTable(schema='intake', table='temp_multi_parent_npis')
    run_stats_DBTable = DBTable(schema='intake', table='temp_run_stats')
    
    # Create SQL execution plan
    sql = FrostDict()
    


    # ========================================
    # PHASE 8: Update NPI-to-ClinicalOrganization relationships
    # ========================================
    
    sql['18_upsert_npi_to_clinical_organization_relationships'] = f"""
    INSERT INTO {npi_to_clinical_org_DBTable} (
        id, 
        npi_id,
        clinical_organization_id,
        primary_authorized_official_individual_id,
        parent_npi_id
    )
    SELECT DISTINCT
        npi_table.id AS id,
        npi_table.id AS npi_id,
        NULL::INTEGER AS clinical_organization_id,
        individual_table.id AS primary_authorized_official_individual_id,
        NULL::INTEGER AS parent_npi_id
    FROM {npi_DBTable} AS npi_table
    JOIN {source_DBTable} AS source_table ON npi_table.npi = source_table."npi"
    JOIN {individual_DBTable} AS individual_table ON (
        individual_table.last_name = COALESCE(source_table."authorized_official_last_name", '')
        AND individual_table.first_name = COALESCE(source_table."authorized_official_first_name", '')
        AND individual_table.middle_name = COALESCE(source_table."authorized_official_middle_name", '')
        AND individual_table.name_prefix = COALESCE(source_table."authorized_official_name_prefix_text", '')
        AND individual_table.name_suffix = COALESCE(source_table."authorized_official_name_suffix_text", '')
    )
    WHERE source_table."entity_type_code" = '2'
    ON CONFLICT (npi_id, clinical_organization_id) DO UPDATE SET
        primary_authorized_official_individual_id = EXCLUDED.primary_authorized_official_individual_id,
        parent_npi_id = EXCLUDED.parent_npi_id;
    """
    
    # ========================================
    # PHASE 9: Log errors
    # ========================================
    
    sql['19_clear_existing_wrongnpi_records'] = f"""
    DELETE FROM {wrongnpi_DBTable} 
    WHERE error_type_string IN ('NO_PARENT', 'MULTI_PARENT')
    AND npi IN (
        SELECT npi FROM {npi_change_log_DBTable} 
        WHERE processed = FALSE
    );
    """
    
    sql['20_log_no_parent_errors'] = f"""
    INSERT INTO {wrongnpi_DBTable} (npi, error_type_string, reason_npi_is_wrong)
    SELECT 
        rp.subpart_npi as npi,
        'NO_PARENT' as error_type_string,
        CONCAT(
            'Organizational subpart NPI has no matching parent organization. ',
            'Parent_Organization_LBN: "', COALESCE(rp."parent_organization_lbn", 'NULL'), '", ',
            'but no non-subpart organization found with matching Legal Business Name.'
        ) as reason_npi_is_wrong
    FROM {resolved_parents_DBTable} rp
    WHERE rp.resolved_parent_npi IS NULL
    AND rp."parent_organization_lbn" IS NOT NULL
    AND rp."parent_organization_lbn" != '';
    """
    
    sql['21_create_multi_parent_npis_temp_table'] = f"""
    DROP TABLE IF EXISTS {multi_parent_npis_DBTable};
    CREATE TABLE {multi_parent_npis_DBTable} AS
    SELECT DISTINCT
        rp.subpart_npi as npi,
        rp."parent_organization_lbn"
    FROM {resolved_parents_DBTable} rp
    WHERE rp.match_count > 1;
    """
    
    sql['22_log_multi_parent_errors'] = f"""
    INSERT INTO {wrongnpi_DBTable} (npi, error_type_string, reason_npi_is_wrong)
    SELECT 
        mp.npi,
        'MULTI_PARENT' as error_type_string,
        CONCAT(
            'Organizational subpart NPI has multiple potential parent organizations. ',
            'Parent_Organization_LBN: "', mp."parent_organization_lbn", '", ',
            'found multiple matching non-subpart organizations with same Legal Business Name.'
        ) as reason_npi_is_wrong
    FROM {multi_parent_npis_DBTable} mp;
    """
    
    # ========================================
    # PHASE 10: Mark changes as processed
    # ========================================
    
    sql['23_mark_npi_changes_as_processed'] = f"""
    UPDATE {npi_change_log_DBTable} 
    SET processed = TRUE 
    WHERE processed = FALSE;
    """
    
    sql['24_mark_individual_changes_as_processed'] = f"""
    UPDATE {individual_change_log_DBTable} 
    SET processed = TRUE 
    WHERE processed = FALSE;
    """
    
    sql['25_mark_parent_changes_as_processed'] = f"""
    UPDATE {parent_change_log_DBTable} 
    SET processed = TRUE 
    WHERE processed = FALSE;
    """
    
    # ========================================
    # PHASE 11: Calculate run statistics and finalize
    # ========================================
    
    sql['26_create_run_stats_temp_table'] = f"""
    DROP TABLE IF EXISTS {run_stats_DBTable};
    CREATE TABLE {run_stats_DBTable} AS
    SELECT 
        COUNT(*) as total_npis_processed,
        COUNT(*) FILTER (WHERE change_type = 'NEW') as new_npis,
        COUNT(*) FILTER (WHERE change_type = 'UPDATED') as updated_npis,
        COUNT(*) FILTER (WHERE change_type = 'DEACTIVATED') as deactivated_npis
    FROM {npi_change_log_DBTable} AS npi_change_log
    JOIN {current_run_DBTable} cr ON npi_change_log.processing_run_id = cr.run_id;
    """
    
    sql['27_finalize_processing_run'] = f"""
    UPDATE {processing_run_DBTable} 
    SET 
        processing_status = 'COMPLETED',
        total_npis_processed = run_stats.total_npis_processed,
        new_npis = run_stats.new_npis,
        updated_npis = run_stats.updated_npis,
        deactivated_npis = run_stats.deactivated_npis,
        notes = 'Data transformation completed successfully. Run Step20 for indexes and Step25 for analysis.'
    FROM {run_stats_DBTable} AS run_stats
    WHERE processing_status = 'IN_PROGRESS';
    """
    
    # Execute SQL pipeline
    print("About to run Incremental Core NPI Pipeline SQL")
    print("=" * 60)
    print("This incremental pipeline will:")
    print("1. Initialize processing run and detect changes")
    print("2. Process only NEW, UPDATED, DEACTIVATED, or REACTIVATED NPIs")
    print("3. Update ndh.NPI table with changed records only")
    print("4. Detect and process Individual record changes")
    print("5. Create new Individual records only when needed")
    print("6. Update NPI-to-Individual relationships")
    print("7. Detect parent relationship changes for organizations")
    print("8. Update NPI-to-ClinicalOrganization relationships")
    print("9. Log parent relationship errors to intake.wrongnpi")
    print("10. Mark all changes as processed")
    print("11. Create performance indexes")
    print("12. Calculate run statistics and finalize")
    print("13. Generate comprehensive summary statistics")
    print("=" * 60)
    print(f"Processing source table: {npi_table}")
    print("=" * 60)
    print("Key Features:")
    print("- No CTEs: Uses intermediate temp tables for clarity")
    print("- Small SQL steps: Each step handles one specific task")
    print("- Incremental updates: Only processes changed records")
    print("- Complete audit trail: All changes logged")
    print("=" * 60)
    
    SQLoopcicle.run_sql_loop(
        sql_dict=sql,
        is_just_print=is_just_print,
        engine=alchemy_engine
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Incremental Core NPI Pipeline failed with error: {e}")
        print("\nMake sure you have installed the required dependencies:")
        print("pip install npd_plainerflow pandas great-expectations")
        print("\nAlso ensure the intake change tracking tables exist:")
        print("Run: sql/create_table_sql/create_intake_npi_changes.sql")
        raise
