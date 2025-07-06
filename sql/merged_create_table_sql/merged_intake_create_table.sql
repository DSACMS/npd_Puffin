-- Merged SQL statements for schema: intake
-- Generated on: 2025-07-06 01:34:37
-- Total statements for this schema: 2
--
-- Source files:
--   sql/create_table_sql/create_intake_phone.sql
--   sql/create_table_sql/create_intake_wrongnpi.sql


-- Source: sql/create_table_sql/create_intake_phone.sql
CREATE TABLE intake.staging_phone (
    id SERIAL PRIMARY KEY,

    -- 1) Raw input exactly as received
    raw_phone          TEXT,                         -- e.g. "(415)555-2671 ext.123"
    is_normalized_success BOOLEAN DEFAULT FALSE,

    -- 2) Parsed components (after Python `phonenumbers`)
    phone_e164         VARCHAR(20),                  -- canonical: "+14155552671"
    country_code       VARCHAR(4),                   -- e.g. "1"
    ndh_PhoneNumber_id  INT DEFAULT NULL, -- link to the unique NDH records for this phone_e164 and country code.   

    raw_phone_extension    VARCHAR(10),                  -- optional: "123"
    ndh_PhoneExtension_id INT, -- link to phone type

    -- 3) Metadata for lineage / debugging
    source_file        TEXT,                         -- feed filename or identifier
    is_fax_in_source   BOOLEAN,
    source_row         INTEGER,                      -- original row number in feed
    ingestion_ts       TIMESTAMPTZ DEFAULT NOW(),    -- when ingested
    error_notes        TEXT,                         -- parser errors or validations
    
    -- Unique constraint to prevent duplicate processing of same raw phone from same source
    CONSTRAINT uc_staging_phone_raw_source UNIQUE (raw_phone, source_file, is_fax_in_source)
);

-- Source: sql/create_table_sql/create_intake_wrongnpi.sql
CREATE TABLE intake.wrongnpi (
    npi BIGINT,
    error_type_string VARCHAR(10),
    reason_npi_is_wrong TEXT
);
