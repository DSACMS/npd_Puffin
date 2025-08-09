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
    # PHASE 0: Create intake tables if they don't exist
    # ========================================
    
    sql['00a_create_npi_processing_run_table'] = f"""
    -- Track processing runs and their metadata
    CREATE TABLE IF NOT EXISTS {processing_run_DBTable} (
        id SERIAL PRIMARY KEY,
        run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source_table VARCHAR(100) NOT NULL,
        total_npis_processed INTEGER,
        new_npis INTEGER,
        updated_npis INTEGER,
        deactivated_npis INTEGER,
        processing_status VARCHAR(50) DEFAULT 'IN_PROGRESS',
        notes TEXT
    );
    """
    
    sql['00b_create_npi_change_log_table'] = f"""
    -- Track individual NPI changes detected during processing
    CREATE TABLE IF NOT EXISTS {npi_change_log_DBTable} (
        id SERIAL PRIMARY KEY,
        processing_run_id INTEGER REFERENCES {processing_run_DBTable}(id),
        npi BIGINT NOT NULL,
        change_type VARCHAR(50) NOT NULL, -- 'NEW', 'UPDATED', 'DEACTIVATED', 'REACTIVATED'
        change_detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        old_last_update_date DATE,
        new_last_update_date DATE,
        change_details JSONB,
        processed BOOLEAN DEFAULT FALSE
    );
    """
    
    sql['00c_create_individual_change_log_table'] = f"""
    -- Track Individual record changes
    CREATE TABLE IF NOT EXISTS {individual_change_log_DBTable} (
        id SERIAL PRIMARY KEY,
        processing_run_id INTEGER REFERENCES {processing_run_DBTable}(id),
        individual_id INTEGER,
        npi BIGINT,
        change_type VARCHAR(50) NOT NULL, -- 'NEW', 'UPDATED', 'NAME_CHANGE'
        change_detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        old_values JSONB,
        new_values JSONB,
        processed BOOLEAN DEFAULT FALSE
    );
    """
    
    sql['00d_create_parent_relationship_change_log_table'] = f"""
    -- Track parent relationship changes for organizations
    CREATE TABLE IF NOT EXISTS {parent_change_log_DBTable} (
        id SERIAL PRIMARY KEY,
        processing_run_id INTEGER REFERENCES {processing_run_DBTable}(id),
        child_npi BIGINT NOT NULL,
        old_parent_npi BIGINT,
        new_parent_npi BIGINT,
        change_type VARCHAR(50) NOT NULL, -- 'NEW_PARENT', 'PARENT_CHANGED', 'PARENT_REMOVED'
        change_detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        processed BOOLEAN DEFAULT FALSE
    );
    """
    
    sql['00e_create_intake_table_indexes'] = f"""
    -- Create indexes for performance on intake tables
    CREATE INDEX IF NOT EXISTS idx_npi_processing_run_date ON {processing_run_DBTable}(run_date);
    CREATE INDEX IF NOT EXISTS idx_npi_change_log_npi ON {npi_change_log_DBTable}(npi);
    CREATE INDEX IF NOT EXISTS idx_npi_change_log_run ON {npi_change_log_DBTable}(processing_run_id);
    CREATE INDEX IF NOT EXISTS idx_npi_change_log_type ON {npi_change_log_DBTable}(change_type);
    CREATE INDEX IF NOT EXISTS idx_individual_change_log_npi ON {individual_change_log_DBTable}(npi);
    CREATE INDEX IF NOT EXISTS idx_parent_relationship_change_log_child ON {parent_change_log_DBTable}(child_npi);
    """
    
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
    CREATE TABLE {current_run_DBTable} AS
    SELECT id AS run_id 
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
    CREATE TABLE {npi_changes_DBTable} AS
    SELECT 
        nppes_main."npi" AS npi,
        nppes_main."last_update_date" AS new_last_update_date,
        npi_table.last_update_date AS old_last_update_date,
        CASE 
            WHEN npi_table.id IS NULL THEN 'NEW'
            WHEN nppes_main."last_update_date" > npi_table.last_update_date THEN 'UPDATED'
            WHEN nppes_main."npi_deactivation_date" IS NOT NULL AND npi_table.deactivation_date IS NULL THEN 'DEACTIVATED'
            WHEN nppes_main."npi_reactivation_date" IS NOT NULL AND npi_table.reactivation_date IS NULL THEN 'REACTIVATED'
            ELSE NULL
        END AS change_type,
        jsonb_build_object(
            'entity_type_code', nppes_main."entity_type_code",
            'deactivation_date', nppes_main."npi_deactivation_date",
            'reactivation_date', nppes_main."npi_reactivation_date",
            'replacement_npi', nppes_main."replacement_npi"
        ) AS change_details
    FROM {source_DBTable} AS nppes_main
    LEFT JOIN {npi_DBTable} AS npi_table ON nppes_main."npi" = npi_table.npi
    WHERE nppes_main."npi" IS NOT NULL;
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
        current_run.run_id,
        npi_changes.npi,
        npi_changes.change_type,
        npi_changes.old_last_update_date,
        npi_changes.new_last_update_date,
        npi_changes.change_details
    FROM {npi_changes_DBTable} AS npi_changes
    CROSS JOIN {current_run_DBTable} AS current_run
    WHERE npi_changes.change_type IS NOT NULL;
    """
    
    # ========================================
    # PHASE 3: Process NPI record changes (UPSERT)
    # ========================================

    # Note This is where we filter out the deactivated NPI records, which have no entity_type_code
    
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
        nppes_main."npi" AS id,
        nppes_main."npi" AS npi,
        nppes_main."entity_type_code"::SMALLINT AS entity_type_code,
        CASE 
            WHEN nppes_main."replacement_npi" IS NOT NULL 
            THEN nppes_main."replacement_npi"::BIGINT
            ELSE NULL 
        END AS replacement_npi,
        nppes_main."provider_enumeration_date" AS enumeration_date,
        nppes_main."last_update_date" AS last_update_date,
        COALESCE(nppes_main."npi_deactivation_reason_code", '') AS deactivation_reason_code,
        nppes_main."npi_deactivation_date" AS deactivation_date,
        nppes_main."npi_reactivation_date" AS reactivation_date,
        nppes_main."certification_date" AS certification_date
    FROM {source_DBTable} AS nppes_main
    WHERE nppes_main."npi" IN (
        SELECT DISTINCT change_log.npi
        FROM {npi_change_log_DBTable} AS change_log
        WHERE change_log.processed = FALSE
        AND change_log.change_type IN ('NEW', 'UPDATED', 'DEACTIVATED', 'REACTIVATED')
    )
    AND nppes_main."entity_type_code" != '' -- filters out deactivated blank records.
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
    CREATE TABLE {individual_provider_changes_DBTable} AS
    SELECT 
        nppes_main."npi" AS npi,
        COALESCE(nppes_main."provider_last_name_legal_name", '') AS last_name,
        COALESCE(nppes_main."provider_first_name", '') AS first_name,
        COALESCE(nppes_main."provider_middle_name", '') AS middle_name,
        COALESCE(nppes_main."provider_name_prefix_text", '') AS name_prefix,
        COALESCE(nppes_main."provider_name_suffix_text", '') AS name_suffix,
        individual_table.id AS existing_individual_id,
        CASE 
            WHEN individual_table.id IS NULL THEN 'NEW'
            WHEN (individual_table.last_name != COALESCE(nppes_main."provider_last_name_legal_name", '') OR
                  individual_table.first_name != COALESCE(nppes_main."provider_first_name", '') OR
                  individual_table.middle_name != COALESCE(nppes_main."provider_middle_name", '') OR
                  individual_table.name_prefix != COALESCE(nppes_main."provider_name_prefix_text", '') OR
                  individual_table.name_suffix != COALESCE(nppes_main."provider_name_suffix_text", '')) THEN 'UPDATED'
            ELSE NULL
        END AS change_type,
        jsonb_build_object(
            'old_last_name', individual_table.last_name,
            'old_first_name', individual_table.first_name,
            'old_middle_name', individual_table.middle_name,
            'old_name_prefix', individual_table.name_prefix,
            'old_name_suffix', individual_table.name_suffix
        ) AS old_values,
        jsonb_build_object(
            'new_last_name', COALESCE(nppes_main."provider_last_name_legal_name", ''),
            'new_first_name', COALESCE(nppes_main."provider_first_name", ''),
            'new_middle_name', COALESCE(nppes_main."provider_middle_name", ''),
            'new_name_prefix', COALESCE(nppes_main."provider_name_prefix_text", ''),
            'new_name_suffix', COALESCE(nppes_main."provider_name_suffix_text", '')
        ) AS new_values
    FROM {source_DBTable} AS nppes_main
    JOIN {npi_change_log_DBTable} AS change_log ON nppes_main."npi" = change_log.npi
    LEFT JOIN {individual_DBTable} AS individual_table ON (
        individual_table.last_name = COALESCE(nppes_main."provider_last_name_legal_name", '')
        AND individual_table.first_name = COALESCE(nppes_main."provider_first_name", '')
        AND individual_table.middle_name = COALESCE(nppes_main."provider_middle_name", '')
        AND individual_table.name_prefix = COALESCE(nppes_main."provider_name_prefix_text", '')
        AND individual_table.name_suffix = COALESCE(nppes_main."provider_name_suffix_text", '')
    )
    WHERE nppes_main."entity_type_code" = '1'
    AND change_log.processed = FALSE
    AND nppes_main."provider_last_name_legal_name" IS NOT NULL
    AND nppes_main."provider_first_name" IS NOT NULL;
    """
    
    sql['07_create_authorized_official_changes_temp_table'] = f"""
    DROP TABLE IF EXISTS {authorized_official_changes_DBTable};
    CREATE TABLE {authorized_official_changes_DBTable} AS
    SELECT 
        nppes_main."npi" AS npi,
        COALESCE(nppes_main."authorized_official_last_name", '') AS last_name,
        COALESCE(nppes_main."authorized_official_first_name", '') AS first_name,
        COALESCE(nppes_main."authorized_official_middle_name", '') AS middle_name,
        COALESCE(nppes_main."authorized_official_name_prefix_text", '') AS name_prefix,
        COALESCE(nppes_main."authorized_official_name_suffix_text", '') AS name_suffix,
        individual_table.id AS existing_individual_id,
        CASE 
            WHEN individual_table.id IS NULL THEN 'NEW'
            WHEN (individual_table.last_name != COALESCE(nppes_main."authorized_official_last_name", '') OR
                  individual_table.first_name != COALESCE(nppes_main."authorized_official_first_name", '') OR
                  individual_table.middle_name != COALESCE(nppes_main."authorized_official_middle_name", '') OR
                  individual_table.name_prefix != COALESCE(nppes_main."authorized_official_name_prefix_text", '') OR
                  individual_table.name_suffix != COALESCE(nppes_main."authorized_official_name_suffix_text", '')) THEN 'UPDATED'
            ELSE NULL
        END AS change_type,
        jsonb_build_object(
            'old_last_name', individual_table.last_name,
            'old_first_name', individual_table.first_name,
            'old_middle_name', individual_table.middle_name,
            'old_name_prefix', individual_table.name_prefix,
            'old_name_suffix', individual_table.name_suffix
        ) AS old_values,
        jsonb_build_object(
            'new_last_name', COALESCE(nppes_main."authorized_official_last_name", ''),
            'new_first_name', COALESCE(nppes_main."authorized_official_first_name", ''),
            'new_middle_name', COALESCE(nppes_main."authorized_official_middle_name", ''),
            'new_name_prefix', COALESCE(nppes_main."authorized_official_name_prefix_text", ''),
            'new_name_suffix', COALESCE(nppes_main."authorized_official_name_suffix_text", '')
        ) AS new_values
    FROM {source_DBTable} AS nppes_main
    JOIN {npi_change_log_DBTable} AS change_log ON nppes_main."npi" = change_log.npi
    LEFT JOIN {individual_DBTable} AS individual_table ON (
        individual_table.last_name = COALESCE(nppes_main."authorized_official_last_name", '')
        AND individual_table.first_name = COALESCE(nppes_main."authorized_official_first_name", '')
        AND individual_table.middle_name = COALESCE(nppes_main."authorized_official_middle_name", '')
        AND individual_table.name_prefix = COALESCE(nppes_main."authorized_official_name_prefix_text", '')
        AND individual_table.name_suffix = COALESCE(nppes_main."authorized_official_name_suffix_text", '')
    )
    WHERE nppes_main."entity_type_code" = '2'
    AND change_log.processed = FALSE
    AND nppes_main."authorized_official_last_name" IS NOT NULL
    AND nppes_main."authorized_official_first_name" IS NOT NULL;
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
        current_run.run_id,
        individual_provider_changes.existing_individual_id,
        individual_provider_changes.npi,
        individual_provider_changes.change_type,
        individual_provider_changes.old_values,
        individual_provider_changes.new_values
    FROM {individual_provider_changes_DBTable} AS individual_provider_changes
    CROSS JOIN {current_run_DBTable} AS current_run
    WHERE individual_provider_changes.change_type IS NOT NULL;
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
        current_run.run_id,
        authorized_official_changes.existing_individual_id,
        authorized_official_changes.npi,
        authorized_official_changes.change_type,
        authorized_official_changes.old_values,
        authorized_official_changes.new_values
    FROM {authorized_official_changes_DBTable} AS authorized_official_changes
    CROSS JOIN {current_run_DBTable} AS current_run
    WHERE authorized_official_changes.change_type IS NOT NULL;
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
        ssn
    )
    SELECT DISTINCT
        individual_provider_changes.last_name,
        individual_provider_changes.first_name,
        individual_provider_changes.middle_name,
        individual_provider_changes.name_prefix,
        individual_provider_changes.name_suffix,
        NULL AS email_address,
        NULL AS ssn
    FROM {individual_provider_changes_DBTable} AS individual_provider_changes
    WHERE individual_provider_changes.change_type = 'NEW'
    AND NOT EXISTS (
        SELECT 1 FROM {individual_DBTable} AS individual_table
        WHERE individual_table.last_name = individual_provider_changes.last_name
        AND individual_table.first_name = individual_provider_changes.first_name
        AND individual_table.middle_name = individual_provider_changes.middle_name
        AND individual_table.name_prefix = individual_provider_changes.name_prefix
        AND individual_table.name_suffix = individual_provider_changes.name_suffix
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
        ssn
    )
    SELECT DISTINCT
        authorized_official_changes.last_name,
        authorized_official_changes.first_name,
        authorized_official_changes.middle_name,
        authorized_official_changes.name_prefix,
        authorized_official_changes.name_suffix,
        NULL AS email_address,
        NULL AS ssn
    FROM {authorized_official_changes_DBTable} AS authorized_official_changes
    WHERE authorized_official_changes.change_type = 'NEW'
    AND NOT EXISTS (
        SELECT 1 FROM {individual_DBTable} AS individual_table
        WHERE individual_table.last_name = authorized_official_changes.last_name
        AND individual_table.first_name = authorized_official_changes.first_name
        AND individual_table.middle_name = authorized_official_changes.middle_name
        AND individual_table.name_prefix = authorized_official_changes.name_prefix
        AND individual_table.name_suffix = authorized_official_changes.name_suffix
    );
    """
    
    # ========================================
    # PHASE 6: Update NPI-to-Individual relationships
    # ========================================
    
    sql['12_upsert_npi_to_individual_relationships'] = f"""
    INSERT INTO {npi_to_individual_DBTable} (
        id,
        npi_id,
        individual_id,
        is_sole_proprietor
    )
    SELECT DISTINCT
        npi_table.id AS id,
        npi_table.id AS npi_id,
        individual_table.id AS individual_id,
        CASE 
            WHEN source_table."is_sole_proprietor" = 'Y' THEN TRUE
            WHEN source_table."is_sole_proprietor" = 'N' THEN FALSE
            ELSE FALSE
        END AS is_sole_proprietor
    FROM {npi_DBTable} AS npi_table
    JOIN {source_DBTable} AS source_table ON npi_table.npi = source_table."npi"
    JOIN {npi_change_log_DBTable} AS change_log ON source_table."npi" = change_log.npi
    JOIN {individual_DBTable} AS individual_table ON (
        individual_table.last_name = COALESCE(source_table."provider_last_name_legal_name", '')
        AND individual_table.first_name = COALESCE(source_table."provider_first_name", '')
        AND individual_table.middle_name = COALESCE(source_table."provider_middle_name", '')
        AND individual_table.name_prefix = COALESCE(source_table."provider_name_prefix_text", '')
        AND individual_table.name_suffix = COALESCE(source_table."provider_name_suffix_text", '')
    )
    WHERE source_table."entity_type_code" = '1'
    AND change_log.processed = FALSE
    ON CONFLICT (npi_id) DO UPDATE SET
        individual_id = EXCLUDED.individual_id,
        is_sole_proprietor = EXCLUDED.is_sole_proprietor;
    """
    
    # ========================================
    # PHASE 7: Detect parent relationship changes
    # ========================================
    
    #TODO better document the purpose of these REGEXP. What is the goal? Why are we doing this? 

    sql['13_create_normalized_org_names_temp_table'] = f"""
    DROP TABLE IF EXISTS {normalized_org_names_DBTable};
    CREATE TABLE {normalized_org_names_DBTable} AS
    SELECT 
        source_table."npi",
        source_table."provider_organization_name_legal_business_name",
        source_table."parent_organization_lbn",
        source_table."is_organization_subpart",
        LOWER(REGEXP_REPLACE(
            COALESCE(source_table."provider_organization_name_legal_business_name", ''), 
            '[^a-zA-Z0-9]', '', 'g'
        )) AS normalized_legal_name,
        LOWER(REGEXP_REPLACE(
            COALESCE(source_table."parent_organization_lbn", ''), 
            '[^a-zA-Z0-9]', '', 'g'
        )) AS normalized_parent_name
    FROM {source_DBTable} AS source_table
    JOIN {npi_change_log_DBTable} AS change_log ON source_table."npi" = change_log.npi
    WHERE source_table."entity_type_code" = '2'
    AND change_log.processed = FALSE;
    """
    
    sql['14_create_parent_matches_temp_table'] = f"""
    DROP TABLE IF EXISTS {parent_matches_DBTable};
    CREATE TABLE {parent_matches_DBTable} AS
    SELECT 
        subpart."npi" as subpart_npi,
        subpart."parent_organization_lbn",
        parent."npi" as parent_npi
    FROM {normalized_org_names_DBTable} subpart
    LEFT JOIN {normalized_org_names_DBTable} parent ON (
        subpart.normalized_parent_name = parent.normalized_legal_name
        AND parent."is_organization_subpart" = 'N'
        AND subpart."npi" != parent."npi"
    )
    WHERE subpart."is_organization_subpart" = 'Y'
    AND subpart.normalized_parent_name != '';
    """
    
    sql['15_create_resolved_parents_temp_table'] = f"""
    DROP TABLE IF EXISTS {resolved_parents_DBTable};
    CREATE TABLE {resolved_parents_DBTable} AS
    SELECT 
        parent_matches.subpart_npi,
        parent_matches."parent_organization_lbn",
        CASE 
            WHEN COUNT(parent_matches.parent_npi) = 1 THEN MAX(parent_matches.parent_npi)
            ELSE NULL
        END AS resolved_parent_npi,
        COUNT(parent_matches.parent_npi) AS match_count
    FROM {parent_matches_DBTable} AS parent_matches
    GROUP BY parent_matches.subpart_npi, parent_matches."parent_organization_lbn";
    """
    
    sql['16_create_parent_changes_temp_table'] = f"""
    DROP TABLE IF EXISTS {parent_changes_DBTable};
    CREATE TABLE {parent_changes_DBTable} AS
    SELECT 
        resolved_parents.subpart_npi AS child_npi,
        npi_to_clinical_org.parent_npi_id AS old_parent_npi,
        resolved_parents.resolved_parent_npi AS new_parent_npi,
        CASE 
            WHEN npi_to_clinical_org.parent_npi_id IS NULL AND resolved_parents.resolved_parent_npi IS NOT NULL THEN 'NEW_PARENT'
            WHEN npi_to_clinical_org.parent_npi_id IS NOT NULL AND resolved_parents.resolved_parent_npi IS NULL THEN 'PARENT_REMOVED'
            WHEN npi_to_clinical_org.parent_npi_id != resolved_parents.resolved_parent_npi THEN 'PARENT_CHANGED'
            ELSE NULL
        END AS change_type
    FROM {resolved_parents_DBTable} AS resolved_parents
    LEFT JOIN {npi_to_clinical_org_DBTable} AS npi_to_clinical_org ON resolved_parents.subpart_npi = npi_to_clinical_org.npi_id;
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
