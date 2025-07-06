#!/usr/bin/env python3
"""
Core NPI Pipeline: Incremental Update of NDH NPI tables from NPPES raw data

This script implements the Core NPI Pipeline with incremental update support for monthly NPPES releases.
It populates three main NDH tables:
1. ndh.NPI - Core NPI records for both individual and organizational providers
2. ndh.NPI_to_Individual - Links individual NPIs to Individual records
3. ndh.NPI_to_ClinicalOrganization - Links organizational NPIs to Clinical Organizations

Key Features:
- Incremental updates: Only processes changed/new NPIs
- Change tracking: Logs all changes to intake tables
- Data preservation: Maintains existing data, only updates what changed
- Monthly processing: Designed for monthly NPPES file releases
- Simple SQL: No CTEs, uses intermediate tables for clarity

Processing phases broken into small, clear steps following DRY principles.
"""

import plainerflow  # type: ignore
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle  # type: ignore
import os

def main():
    # Control dry-run mode - start with True to preview SQL
    is_just_print = True
    
    print("Connecting to DB")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)
    
    # Define source and target tables
    npi_table = 'main_file_small'  # For testing
    #npi_table = 'main_file'  # For production
    source_DBTable = DBTable(schema='nppes_raw', table=npi_table)
    
    # Target NDH tables
    npi_DBTable = DBTable(schema='ndh', table='NPI')
    individual_DBTable = DBTable(schema='ndh', table='Individual')
    npi_to_individual_DBTable = DBTable(schema='ndh', table='NPI_to_Individual')
    npi_to_clinical_org_DBTable = DBTable(schema='ndh', table='NPI_to_ClinicalOrganization')
    wrongnpi_DBTable = DBTable(schema='intake', table='wrongnpi')
    
    # Intake tracking tables
    processing_run_DBTable = DBTable(schema='intake', table='npi_processing_run')
    npi_change_log_DBTable = DBTable(schema='intake', table='npi_change_log')
    individual_change_log_DBTable = DBTable(schema='intake', table='individual_change_log')
    parent_change_log_DBTable = DBTable(schema='intake', table='parent_relationship_change_log')
    
    # Intermediate working tables
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
    # PHASE 1: Initialize processing run
    # ========================================
    
    sql['01_start_processing_run'] = f"""
    INSERT INTO {processing_run_DBTable} (
        source_table,
        processing_status,
        notes
    )
    VALUES (
        '{npi_table}',
        'IN_PROGRESS',
        'Starting incremental NPI processing run'
    );
    """
    
    sql['02_create_current_run_temp_table'] = f"""
    DROP TABLE IF EXISTS {current_run_DBTable};
    CREATE TEMP TABLE {current_run_DBTable} AS
    SELECT id as run_id 
    FROM {processing_run_DBTable} 
    WHERE processing_status = 'IN_PROGRESS' 
    ORDER BY run_date DESC 
    LIMIT 1;
    """
    
    # ========================================
    # PHASE 2: Detect NPI changes
    # ========================================
    
    sql['03_create_npi_changes_temp_table'] = f"""
    DROP TABLE IF EXISTS {npi_changes_DBTable};
    CREATE TEMP TABLE {npi_changes_DBTable} AS
    SELECT 
        s."NPI" as npi,
        s."Last_Update_Date" as new_last_update_date,
        n.last_update_date as old_last_update_date,
        CASE 
            WHEN n.id IS NULL THEN 'NEW'
            WHEN s."Last_Update_Date" > n.last_update_date THEN 'UPDATED'
            WHEN s."NPI_Deactivation_Date" IS NOT NULL AND n.deactivation_date IS NULL THEN 'DEACTIVATED'
            WHEN s."NPI_Reactivation_Date" IS NOT NULL AND n.reactivation_date IS NULL THEN 'REACTIVATED'
            ELSE NULL
        END as change_type,
        jsonb_build_object(
            'entity_type_code', s."Entity_Type_Code",
            'deactivation_date', s."NPI_Deactivation_Date",
            'reactivation_date', s."NPI_Reactivation_Date",
            'replacement_npi', s."Replacement_NPI"
        ) as change_details
    FROM {source_DBTable} s
    LEFT JOIN {npi_DBTable} n ON s."NPI" = n.npi
    WHERE s."NPI" IS NOT NULL;
    """
    
    sql['04_log_npi_changes'] = f"""
    INSERT INTO {npi_change_log_DBTable} (
        processing_run_id,
        npi,
        change_type,
        old_last_update_date,
        new_last_update_date,
        change_details
    )
    SELECT 
        cr.run_id,
        nc.npi,
        nc.change_type,
        nc.old_last_update_date,
        nc.new_last_update_date,
        nc.change_details
    FROM {npi_changes_DBTable} nc
    CROSS JOIN {current_run_DBTable} cr
    WHERE nc.change_type IS NOT NULL;
    """
    
    # ========================================
    # PHASE 3: Process NPI record changes (UPSERT)
    # ========================================
    
    sql['05_upsert_npi_records'] = f"""
    INSERT INTO {npi_DBTable} (
        id,
        npi,
        entity_type_code,
        replacement_npi,
        enumeration_date,
        last_update_date,
        deactivation_reason_code,
        deactivation_date,
        reactivation_date,
        certification_date
    )
    SELECT 
        s."NPI" as id,
        s."NPI" as npi,
        s."Entity_Type_Code"::SMALLINT as entity_type_code,
        CASE 
            WHEN s."Replacement_NPI" IS NOT NULL 
            THEN s."Replacement_NPI"::VARCHAR(11)
            ELSE NULL 
        END as replacement_npi,
        s."Provider_Enumeration_Date" as enumeration_date,
        s."Last_Update_Date" as last_update_date,
        COALESCE(s."NPI_Deactivation_Reason_Code", '') as deactivation_reason_code,
        s."NPI_Deactivation_Date" as deactivation_date,
        s."NPI_Reactivation_Date" as reactivation_date,
        s."Certification_Date" as certification_date
    FROM {source_DBTable} s
    JOIN {npi_change_log_DBTable} cl ON s."NPI" = cl.npi
    WHERE cl.processed = FALSE
    AND cl.change_type IN ('NEW', 'UPDATED', 'DEACTIVATED', 'REACTIVATED')
    ON CONFLICT (id) DO UPDATE SET
        entity_type_code = EXCLUDED.entity_type_code,
        replacement_npi = EXCLUDED.replacement_npi,
        enumeration_date = EXCLUDED.enumeration_date,
        last_update_date = EXCLUDED.last_update_date,
        deactivation_reason_code = EXCLUDED.deactivation_reason_code,
        deactivation_date = EXCLUDED.deactivation_date,
        reactivation_date = EXCLUDED.reactivation_date,
        certification_date = EXCLUDED.certification_date;
    """
    
    # ========================================
    # PHASE 4: Detect Individual record changes
    # ========================================
    
    sql['06_create_individual_provider_changes_temp_table'] = f"""
    DROP TABLE IF EXISTS {individual_provider_changes_DBTable};
    CREATE TEMP TABLE {individual_provider_changes_DBTable} AS
    SELECT 
        s."NPI" as npi,
        COALESCE(s."Provider_Last_Name_Legal_Name", '') as last_name,
        COALESCE(s."Provider_First_Name", '') as first_name,
        COALESCE(s."Provider_Middle_Name", '') as middle_name,
        COALESCE(s."Provider_Name_Prefix_Text", '') as name_prefix,
        COALESCE(s."Provider_Name_Suffix_Text", '') as name_suffix,
        i.id as existing_individual_id,
        CASE 
            WHEN i.id IS NULL THEN 'NEW'
            WHEN (i.last_name != COALESCE(s."Provider_Last_Name_Legal_Name", '') OR
                  i.first_name != COALESCE(s."Provider_First_Name", '') OR
                  i.middle_name != COALESCE(s."Provider_Middle_Name", '') OR
                  i.name_prefix != COALESCE(s."Provider_Name_Prefix_Text", '') OR
                  i.name_suffix != COALESCE(s."Provider_Name_Suffix_Text", '')) THEN 'UPDATED'
            ELSE NULL
        END as change_type,
        jsonb_build_object(
            'old_last_name', i.last_name,
            'old_first_name', i.first_name,
            'old_middle_name', i.middle_name,
            'old_name_prefix', i.name_prefix,
            'old_name_suffix', i.name_suffix
        ) as old_values,
        jsonb_build_object(
            'new_last_name', COALESCE(s."Provider_Last_Name_Legal_Name", ''),
            'new_first_name', COALESCE(s."Provider_First_Name", ''),
            'new_middle_name', COALESCE(s."Provider_Middle_Name", ''),
            'new_name_prefix', COALESCE(s."Provider_Name_Prefix_Text", ''),
            'new_name_suffix', COALESCE(s."Provider_Name_Suffix_Text", '')
        ) as new_values
    FROM {source_DBTable} s
    JOIN {npi_change_log_DBTable} cl ON s."NPI" = cl.npi
    LEFT JOIN {individual_DBTable} i ON (
        i.last_name = COALESCE(s."Provider_Last_Name_Legal_Name", '')
        AND i.first_name = COALESCE(s."Provider_First_Name", '')
        AND i.middle_name = COALESCE(s."Provider_Middle_Name", '')
        AND i.name_prefix = COALESCE(s."Provider_Name_Prefix_Text", '')
        AND i.name_suffix = COALESCE(s."Provider_Name_Suffix_Text", '')
    )
    WHERE s."Entity_Type_Code" = '1'
    AND cl.processed = FALSE
    AND s."Provider_Last_Name_Legal_Name" IS NOT NULL
    AND s."Provider_First_Name" IS NOT NULL;
    """
    
    sql['07_create_authorized_official_changes_temp_table'] = f"""
    DROP TABLE IF EXISTS {authorized_official_changes_DBTable};
    CREATE TEMP TABLE {authorized_official_changes_DBTable} AS
    SELECT 
        s."NPI" as npi,
        COALESCE(s."Authorized_Official_Last_Name", '') as last_name,
        COALESCE(s."Authorized_Official_First_Name", '') as first_name,
        COALESCE(s."Authorized_Official_Middle_Name", '') as middle_name,
        COALESCE(s."Authorized_Official_Name_Prefix_Text", '') as name_prefix,
        COALESCE(s."Authorized_Official_Name_Suffix_Text", '') as name_suffix,
        i.id as existing_individual_id,
        CASE 
            WHEN i.id IS NULL THEN 'NEW'
            WHEN (i.last_name != COALESCE(s."Authorized_Official_Last_Name", '') OR
                  i.first_name != COALESCE(s."Authorized_Official_First_Name", '') OR
                  i.middle_name != COALESCE(s."Authorized_Official_Middle_Name", '') OR
                  i.name_prefix != COALESCE(s."Authorized_Official_Name_Prefix_Text", '') OR
                  i.name_suffix != COALESCE(s."Authorized_Official_Name_Suffix_Text", '')) THEN 'UPDATED'
            ELSE NULL
        END as change_type,
        jsonb_build_object(
            'old_last_name', i.last_name,
            'old_first_name', i.first_name,
            'old_middle_name', i.middle_name,
            'old_name_prefix', i.name_prefix,
            'old_name_suffix', i.name_suffix
        ) as old_values,
        jsonb_build_object(
            'new_last_name', COALESCE(s."Authorized_Official_Last_Name", ''),
            'new_first_name', COALESCE(s."Authorized_Official_First_Name", ''),
            'new_middle_name', COALESCE(s."Authorized_Official_Middle_Name", ''),
            'new_name_prefix', COALESCE(s."Authorized_Official_Name_Prefix_Text", ''),
            'new_name_suffix', COALESCE(s."Authorized_Official_Name_Suffix_Text", '')
        ) as new_values
    FROM {source_DBTable} s
    JOIN {npi_change_log_DBTable} cl ON s."NPI" = cl.npi
    LEFT JOIN {individual_DBTable} i ON (
        i.last_name = COALESCE(s."Authorized_Official_Last_Name", '')
        AND i.first_name = COALESCE(s."Authorized_Official_First_Name", '')
        AND i.middle_name = COALESCE(s."Authorized_Official_Middle_Name", '')
        AND i.name_prefix = COALESCE(s."Authorized_Official_Name_Prefix_Text", '')
        AND i.name_suffix = COALESCE(s."Authorized_Official_Name_Suffix_Text", '')
    )
    WHERE s."Entity_Type_Code" = '2'
    AND cl.processed = FALSE
    AND s."Authorized_Official_Last_Name" IS NOT NULL
    AND s."Authorized_Official_First_Name" IS NOT NULL;
    """
    
    sql['08_log_individual_provider_changes'] = f"""
    INSERT INTO {individual_change_log_DBTable} (
        processing_run_id,
        individual_id,
        npi,
        change_type,
        old_values,
        new_values
    )
    SELECT 
        cr.run_id,
        ipc.existing_individual_id,
        ipc.npi,
        ipc.change_type,
        ipc.old_values,
        ipc.new_values
    FROM {individual_provider_changes_DBTable} ipc
    CROSS JOIN {current_run_DBTable} cr
    WHERE ipc.change_type IS NOT NULL;
    """
    
    sql['09_log_authorized_official_changes'] = f"""
    INSERT INTO {individual_change_log_DBTable} (
        processing_run_id,
        individual_id,
        npi,
        change_type,
        old_values,
        new_values
    )
    SELECT 
        cr.run_id,
        aoc.existing_individual_id,
        aoc.npi,
        aoc.change_type,
        aoc.old_values,
        aoc.new_values
    FROM {authorized_official_changes_DBTable} aoc
    CROSS JOIN {current_run_DBTable} cr
    WHERE aoc.change_type IS NOT NULL;
    """
    
    # ========================================
    # PHASE 5: Create new Individual records
    # ========================================
    
    sql['10_insert_new_individual_records_from_providers'] = f"""
    INSERT INTO {individual_DBTable} (
        last_name,
        first_name,
        middle_name,
        name_prefix,
        name_suffix,
        email_address,
        SSN
    )
    SELECT DISTINCT
        ipc.last_name,
        ipc.first_name,
        ipc.middle_name,
        ipc.name_prefix,
        ipc.name_suffix,
        NULL as email_address,
        NULL as SSN
    FROM {individual_provider_changes_DBTable} ipc
    WHERE ipc.change_type = 'NEW'
    AND NOT EXISTS (
        SELECT 1 FROM {individual_DBTable} i
        WHERE i.last_name = ipc.last_name
        AND i.first_name = ipc.first_name
        AND i.middle_name = ipc.middle_name
        AND i.name_prefix = ipc.name_prefix
        AND i.name_suffix = ipc.name_suffix
    );
    """
    
    sql['11_insert_new_individual_records_from_officials'] = f"""
    INSERT INTO {individual_DBTable} (
        last_name,
        first_name,
        middle_name,
        name_prefix,
        name_suffix,
        email_address,
        SSN
    )
    SELECT DISTINCT
        aoc.last_name,
        aoc.first_name,
        aoc.middle_name,
        aoc.name_prefix,
        aoc.name_suffix,
        NULL as email_address,
        NULL as SSN
    FROM {authorized_official_changes_DBTable} aoc
    WHERE aoc.change_type = 'NEW'
    AND NOT EXISTS (
        SELECT 1 FROM {individual_DBTable} i
        WHERE i.last_name = aoc.last_name
        AND i.first_name = aoc.first_name
        AND i.middle_name = aoc.middle_name
        AND i.name_prefix = aoc.name_prefix
        AND i.name_suffix = aoc.name_suffix
    );
    """
    
    # ========================================
    # PHASE 6: Update NPI-to-Individual relationships
    # ========================================
    
    sql['12_upsert_npi_to_individual_relationships'] = f"""
    INSERT INTO {npi_to_individual_DBTable} (
        NPI_id,
        Individual_id,
        is_sole_proprietor,
        sex_code
    )
    SELECT 
        n.id::INT as NPI_id,
        i.id as Individual_id,
        CASE 
            WHEN s."Is_Sole_Proprietor" = 'Y' THEN TRUE
            WHEN s."Is_Sole_Proprietor" = 'N' THEN FALSE
            ELSE FALSE
        END as is_sole_proprietor,
        COALESCE(s."Provider_Sex_Code", '') as sex_code
    FROM {npi_DBTable} n
    JOIN {source_DBTable} s ON n.npi = s."NPI"
    JOIN {npi_change_log_DBTable} cl ON s."NPI" = cl.npi
    JOIN {individual_DBTable} i ON (
        i.last_name = COALESCE(s."Provider_Last_Name_Legal_Name", '')
        AND i.first_name = COALESCE(s."Provider_First_Name", '')
        AND i.middle_name = COALESCE(s."Provider_Middle_Name", '')
        AND i.name_prefix = COALESCE(s."Provider_Name_Prefix_Text", '')
        AND i.name_suffix = COALESCE(s."Provider_Name_Suffix_Text", '')
    )
    WHERE s."Entity_Type_Code" = '1'
    AND cl.processed = FALSE
    ON CONFLICT (NPI_id) DO UPDATE SET
        Individual_id = EXCLUDED.Individual_id,
        is_sole_proprietor = EXCLUDED.is_sole_proprietor,
        sex_code = EXCLUDED.sex_code;
    """
    
    # ========================================
    # PHASE 7: Detect parent relationship changes
    # ========================================
    
    #TODO better document the purpose of these REGEXP. What is the goal? Why are we doing this? 

    sql['13_create_normalized_org_names_temp_table'] = f"""
    DROP TABLE IF EXISTS {normalized_org_names_DBTable};
    CREATE TEMP TABLE {normalized_org_names_DBTable} AS
    SELECT 
        s."NPI",
        s."Provider_Organization_Name_Legal_Business_Name",
        s."Parent_Organization_LBN",
        s."Is_Organization_Subpart",
        LOWER(REGEXP_REPLACE(
            COALESCE(s."Provider_Organization_Name_Legal_Business_Name", ''), 
            '[^a-zA-Z0-9]', '', 'g'
        )) as normalized_legal_name,
        LOWER(REGEXP_REPLACE(
            COALESCE(s."Parent_Organization_LBN", ''), 
            '[^a-zA-Z0-9]', '', 'g'
        )) as normalized_parent_name
    FROM {source_DBTable} s
    JOIN {npi_change_log_DBTable} cl ON s."NPI" = cl.npi
    WHERE s."Entity_Type_Code" = '2'
    AND cl.processed = FALSE;
    """
    
    sql['14_create_parent_matches_temp_table'] = f"""
    DROP TABLE IF EXISTS {parent_matches_DBTable};
    CREATE TEMP TABLE {parent_matches_DBTable} AS
    SELECT 
        subpart."NPI" as subpart_npi,
        subpart."Parent_Organization_LBN",
        parent."NPI" as parent_npi
    FROM {normalized_org_names_DBTable} subpart
    LEFT JOIN {normalized_org_names_DBTable} parent ON (
        subpart.normalized_parent_name = parent.normalized_legal_name
        AND parent."Is_Organization_Subpart" = 'N'
        AND subpart."NPI" != parent."NPI"
    )
    WHERE subpart."Is_Organization_Subpart" = 'Y'
    AND subpart.normalized_parent_name != '';
    """
    
    sql['15_create_resolved_parents_temp_table'] = f"""
    DROP TABLE IF EXISTS {resolved_parents_DBTable};
    CREATE TEMP TABLE {resolved_parents_DBTable} AS
    SELECT 
        pm.subpart_npi,
        pm."Parent_Organization_LBN",
        CASE 
            WHEN COUNT(pm.parent_npi) = 1 THEN MAX(pm.parent_npi)
            ELSE NULL
        END as resolved_parent_npi,
        COUNT(pm.parent_npi) as match_count
    FROM {parent_matches_DBTable} pm
    GROUP BY pm.subpart_npi, pm."Parent_Organization_LBN";
    """
    
    sql['16_create_parent_changes_temp_table'] = f"""
    DROP TABLE IF EXISTS {parent_changes_DBTable};
    CREATE TEMP TABLE {parent_changes_DBTable} AS
    SELECT 
        rp.subpart_npi as child_npi,
        nco.Parent_NPI_id as old_parent_npi,
        rp.resolved_parent_npi as new_parent_npi,
        CASE 
            WHEN nco.Parent_NPI_id IS NULL AND rp.resolved_parent_npi IS NOT NULL THEN 'NEW_PARENT'
            WHEN nco.Parent_NPI_id IS NOT NULL AND rp.resolved_parent_npi IS NULL THEN 'PARENT_REMOVED'
            WHEN nco.Parent_NPI_id != rp.resolved_parent_npi THEN 'PARENT_CHANGED'
            ELSE NULL
        END as change_type
    FROM {resolved_parents_DBTable} rp
    LEFT JOIN {npi_to_clinical_org_DBTable} nco ON rp.subpart_npi = nco.NPI_id;
    """
    
    sql['17_log_parent_relationship_changes'] = f"""
    INSERT INTO {parent_change_log_DBTable} (
        processing_run_id,
        child_npi,
        old_parent_npi,
        new_parent_npi,
        change_type
    )
    SELECT 
        cr.run_id,
        pc.child_npi,
        pc.old_parent_npi,
        pc.new_parent_npi,
        pc.change_type
    FROM {parent_changes_DBTable} pc
    CROSS JOIN {current_run_DBTable} cr
    WHERE pc.change_type IS NOT NULL;
    """
    
    # ========================================
    # PHASE 8: Update NPI-to-ClinicalOrganization relationships
    # ========================================
    
    sql['18_upsert_npi_to_clinical_organization_relationships'] = f"""
    INSERT INTO {npi_to_clinical_org_DBTable} (
        NPI_id,
        ClinicalOrganization_id,
        PrimaryAuthorizedOfficial_Individual_id,
        Parent_NPI_id
    )
    SELECT 
        n.npi as NPI_id,
        NULL as ClinicalOrganization_id,
        i.id as PrimaryAuthorizedOfficial_Individual_id,
        pcl.new_parent_npi as Parent_NPI_id
    FROM {npi_DBTable} n
    JOIN {source_DBTable} s ON n.npi = s."NPI"
    JOIN {npi_change_log_DBTable} cl ON s."NPI" = cl.npi
    JOIN {individual_DBTable} i ON (
        i.last_name = COALESCE(s."Authorized_Official_Last_Name", '')
        AND i.first_name = COALESCE(s."Authorized_Official_First_Name", '')
        AND i.middle_name = COALESCE(s."Authorized_Official_Middle_Name", '')
        AND i.name_prefix = COALESCE(s."Authorized_Official_Name_Prefix_Text", '')
        AND i.name_suffix = COALESCE(s."Authorized_Official_Name_Suffix_Text", '')
    )
    LEFT JOIN {parent_change_log_DBTable} pcl ON n.npi = pcl.child_npi AND pcl.processed = FALSE
    WHERE s."Entity_Type_Code" = '2'
    AND cl.processed = FALSE
    ON CONFLICT (NPI_id) DO UPDATE SET
        PrimaryAuthorizedOfficial_Individual_id = EXCLUDED.PrimaryAuthorizedOfficial_Individual_id,
        Parent_NPI_id = EXCLUDED.Parent_NPI_id;
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
            'Parent_Organization_LBN: "', COALESCE(rp."Parent_Organization_LBN", 'NULL'), '", ',
            'but no non-subpart organization found with matching Legal Business Name.'
        ) as reason_npi_is_wrong
    FROM {resolved_parents_DBTable} rp
    WHERE rp.resolved_parent_npi IS NULL
    AND rp."Parent_Organization_LBN" IS NOT NULL
    AND rp."Parent_Organization_LBN" != '';
    """
    
    sql['21_create_multi_parent_npis_temp_table'] = f"""
    DROP TABLE IF EXISTS {multi_parent_npis_DBTable};
    CREATE TEMP TABLE {multi_parent_npis_DBTable} AS
    SELECT DISTINCT
        rp.subpart_npi as npi,
        rp."Parent_Organization_LBN"
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
            'Parent_Organization_LBN: "', mp."Parent_Organization_LBN", '", ',
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
    CREATE TEMP TABLE {run_stats_DBTable} AS
    SELECT 
        COUNT(*) as total_npis_processed,
        COUNT(*) FILTER (WHERE change_type = 'NEW') as new_npis,
        COUNT(*) FILTER (WHERE change_type = 'UPDATED') as updated_npis,
        COUNT(*) FILTER (WHERE change_type = 'DEACTIVATED') as deactivated_npis
    FROM {npi_change_log_DBTable} ncl
    JOIN {current_run_DBTable} cr ON ncl.processing_run_id = cr.run_id;
    """
    
    sql['27_finalize_processing_run'] = f"""
    UPDATE {processing_run_DBTable} 
    SET 
        processing_status = 'COMPLETED',
        total_npis_processed = rs.total_npis_processed,
        new_npis = rs.new_npis,
        updated_npis = rs.updated_npis,
        deactivated_npis = rs.deactivated_npis,
        notes = 'Data transformation completed successfully. Run Step20 for indexes and Step25 for analysis.'
    FROM {run_stats_DBTable} rs
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
        print("pip install plainerflow pandas great-expectations")
        print("\nAlso ensure the intake change tracking tables exist:")
        print("Run: sql/create_table_sql/create_intake_npi_changes.sql")
        raise
