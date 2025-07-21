#!/usr/bin/env python3
"""
ETL Pipeline Step: Import Raw Addresses from NPPES Source Files

This script extracts mailing, practice, affiliation, and secondary practice
addresses from the raw NPPES data, computes a hash for each unique address,
and populates the normalized address tables in the 'ndh' schema.

It uses a persistent mapping table (`intake.raw_address_import_map`) to
avoid re-processing addresses that have already been imported in previous runs.
"""

import os
from plainerflow import CredentialFinder, DBTable, FrostDict, SQLoopcicle

def main():
    """
    Main function to execute the ETL pipeline.
    """
    # Set to True to preview SQL statements without executing them
    is_just_print = True

    print("Connecting to the database...")
    base_path = os.path.dirname(os.path.abspath(__file__))
    env_location = os.path.abspath(os.path.join(base_path, "..", "..", ".env"))
    alchemy_engine = CredentialFinder.detect_config(verbose=True, env_path=env_location)

    # Define source and destination tables
    nppes_main_DBTable = DBTable(schema='nppes_raw', table='main_file')
    nppes_endpoint_DBTable = DBTable(schema='nppes_raw', table='endpoint')
    nppes_pl_DBTable = DBTable(schema='nppes_raw', table='pl_file')

    address_DBTable = DBTable(schema='ndh', table='address')
    address_us_DBTable = DBTable(schema='ndh', table='address_us')
    address_intl_DBTable = DBTable(schema='ndh', table='address_international')
    npi_address_DBTable = DBTable(schema='ndh', table='npi_address')

    # Define temporary and mapping tables
    raw_import_DBTable = DBTable(schema='intake', table='raw_address_import')
    import_map_DBTable = DBTable(schema='intake', table='raw_address_import_map')
    not_mapped_DBTable = DBTable(schema='intake', table='address_not_mapped')

    sql = FrostDict()

    sql['create_map_table'] = f"""
    CREATE TABLE IF NOT EXISTS {import_map_DBTable} (
        address_hash VARCHAR(32) PRIMARY KEY,
        address_id INT NOT NULL
    );
    """

    sql['aggregate_raw_addresses'] = f"""
    DROP TABLE IF EXISTS {raw_import_DBTable};
    CREATE TABLE {raw_import_DBTable} AS
    SELECT
        npi,
        2 AS address_type_id,
        provider_first_line_business_mailing_address AS address_line_1,
        provider_second_line_business_mailing_address AS address_line_2,
        provider_business_mailing_address_city_name AS city,
        provider_business_mailing_address_state_name AS state,
        provider_business_mailing_address_postal_code AS postal_code,
        provider_business_mailing_address_country_code AS country_code,
        MD5(
            LOWER(
                COALESCE(provider_first_line_business_mailing_address, '') ||
                COALESCE(provider_second_line_business_mailing_address, '') ||
                COALESCE(provider_business_mailing_address_city_name, '') ||
                COALESCE(provider_business_mailing_address_state_name, '') ||
                COALESCE(provider_business_mailing_address_postal_code, '') ||
                COALESCE(provider_business_mailing_address_country_code, '')
            )
        ) AS address_hash
    FROM
        {nppes_main_DBTable}
    WHERE
        provider_first_line_business_mailing_address IS NOT NULL

    UNION ALL

    SELECT
        npi,
        1 AS address_type_id,
        provider_first_line_business_practice_location_address AS address_line_1,
        provider_second_line_business_practice_location_address AS address_line_2,
        provider_business_practice_location_address_city_name AS city,
        provider_business_practice_location_address_state_name AS state,
        provider_business_practice_location_address_postal_code AS postal_code,
        provider_business_practice_location_address_country_code AS country_code,
        MD5(
            LOWER(
                COALESCE(provider_first_line_business_practice_location_address, '') ||
                COALESCE(provider_second_line_business_practice_location_address, '') ||
                COALESCE(provider_business_practice_location_address_city_name, '') ||
                COALESCE(provider_business_practice_location_address_state_name, '') ||
                COALESCE(provider_business_practice_location_address_postal_code, '') ||
                COALESCE(provider_business_practice_location_address_country_code, '')
            )
        ) AS address_hash
    FROM
        {nppes_main_DBTable}
    WHERE
        provider_first_line_business_practice_location_address IS NOT NULL

    UNION ALL

    SELECT
        npi,
        3 AS address_type_id,
        affiliation_address_line_1 AS address_line_1,
        affiliation_address_line_2 AS address_line_2,
        affiliation_address_city AS city,
        affiliation_address_state AS state,
        affiliation_address_postal_code AS postal_code,
        affiliation_address_country AS country_code,
        MD5(
            LOWER(
                COALESCE(affiliation_address_line_1, '') ||
                COALESCE(affiliation_address_line_2, '') ||
                COALESCE(affiliation_address_city, '') ||
                COALESCE(affiliation_address_state, '') ||
                COALESCE(affiliation_address_postal_code, '') ||
                COALESCE(affiliation_address_country, '')
            )
        ) AS address_hash
    FROM
        {nppes_endpoint_DBTable}
    WHERE
        affiliation_address_line_1 IS NOT NULL

    UNION ALL

    SELECT
        npi,
        4 AS address_type_id,
        provider_secondary_practice_address_address_line_1 AS address_line_1,
        provider_secondary_practice_address_address_line_2 AS address_line_2,
        provider_secondary_practice_address_city_name AS city,
        provider_secondary_practice_address_state_name AS state,
        provider_secondary_practice_address_postal_code AS postal_code,
        provider_secondary_practice_address_country_code AS country_code,
        MD5(
            LOWER(
                COALESCE(provider_secondary_practice_address_address_line_1, '') ||
                COALESCE(provider_secondary_practice_address_address_line_2, '') ||
                COALESCE(provider_secondary_practice_address_city_name, '') ||
                COALESCE(provider_secondary_practice_address_state_name, '') ||
                COALESCE(provider_secondary_practice_address_postal_code, '') ||
                COALESCE(provider_secondary_practice_address_country_code, '')
            )
        ) AS address_hash
    FROM
        {nppes_pl_DBTable}
    WHERE
        provider_secondary_practice_address_address_line_1 IS NOT NULL;
    """

    sql['identify_unmapped_addresses'] = f"""
    DROP TABLE IF EXISTS {not_mapped_DBTable};
    CREATE TABLE {not_mapped_DBTable} AS
    SELECT DISTINCT
        t1.address_line_1,
        t1.address_line_2,
        t1.city,
        t1.state,
        t1.postal_code,
        t1.country_code,
        t1.address_hash
    FROM
        {raw_import_DBTable} AS t1
    LEFT JOIN
        {import_map_DBTable} AS t2
    ON
        t1.address_hash = t2.address_hash
    WHERE
        t2.address_id IS NULL;
    """

    sql['insert_us_addresses'] = f"""
    INSERT INTO {address_us_DBTable} (
        delivery_line_1,
        delivery_line_2,
        city_name,
        state_abbreviation,
        zipcode
    )
    SELECT
        address_line_1,
        address_line_2,
        city,
        state,
        postal_code
    FROM
        {not_mapped_DBTable}
    WHERE
        country_code IS NULL OR country_code = '' OR country_code = 'US';
    """

    sql['insert_international_addresses'] = f"""
    INSERT INTO {address_intl_DBTable} (
        address1,
        address2,
        locality,
        administrative_area,
        postal_code,
        country
    )
    SELECT
        address_line_1,
        address_line_2,
        city,
        state,
        postal_code,
        country_code
    FROM
        {not_mapped_DBTable}
    WHERE
        country_code IS NOT NULL AND country_code != '' AND country_code != 'US';
    """

    sql['populate_main_address_table_us'] = f"""
    INSERT INTO {address_DBTable} (address_us_id)
    SELECT us.id
    FROM {address_us_DBTable} AS us
    JOIN {not_mapped_DBTable} AS nm
        ON us.delivery_line_1 = nm.address_line_1
        AND COALESCE(us.delivery_line_2, '') = COALESCE(nm.address_line_2, '')
        AND us.city_name = nm.city
        AND us.state_abbreviation = nm.state
        AND us.zipcode = nm.postal_code
    LEFT JOIN {address_DBTable} a ON a.address_us_id = us.id
    WHERE (nm.country_code IS NULL OR nm.country_code = '' OR nm.country_code = 'US')
    AND a.id IS NULL;
    """

    sql['populate_main_address_table_intl'] = f"""
    INSERT INTO {address_DBTable} (address_international_id)
    SELECT intl.id
    FROM {address_intl_DBTable} AS intl
    JOIN {not_mapped_DBTable} AS nm
        ON intl.address1 = nm.address_line_1
        AND COALESCE(intl.address2, '') = COALESCE(nm.address_line_2, '')
        AND intl.locality = nm.city
        AND intl.administrative_area = nm.state
        AND intl.postal_code = nm.postal_code
        AND intl.country = nm.country_code
    LEFT JOIN {address_DBTable} a ON a.address_international_id = intl.id
    WHERE (nm.country_code IS NOT NULL AND nm.country_code != '' AND nm.country_code != 'US')
    AND a.id IS NULL;
    """

    sql['update_import_map'] = f"""
    INSERT INTO {import_map_DBTable} (address_hash, address_id)
    SELECT
        nm.address_hash,
        a.id
    FROM {not_mapped_DBTable} AS nm
    JOIN {address_DBTable} AS a
        ON (a.address_us_id IN (SELECT id FROM {address_us_DBTable} us WHERE us.delivery_line_1 = nm.address_line_1 AND COALESCE(us.delivery_line_2, '') = COALESCE(nm.address_line_2, '') AND us.city_name = nm.city AND us.state_abbreviation = nm.state AND us.zipcode = nm.postal_code))
        OR (a.address_international_id IN (SELECT id FROM {address_intl_DBTable} intl WHERE intl.address1 = nm.address_line_1 AND COALESCE(intl.address2, '') = COALESCE(nm.address_line_2, '') AND intl.locality = nm.city AND intl.administrative_area = nm.state AND intl.postal_code = nm.postal_code AND intl.country = nm.country_code))
    ON CONFLICT (address_hash) DO NOTHING;
    """

    # --- SQL implementation will be added here in subsequent steps ---

    print("Executing SQL pipeline...")
    SQLoopcicle.run_sql_loop(
        sql_dict=sql,
        is_just_print=is_just_print,
        engine=alchemy_engine
    )
    print("Pipeline finished.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        raise
