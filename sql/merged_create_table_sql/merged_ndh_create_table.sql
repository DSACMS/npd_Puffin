-- Merged SQL statements for schema: ndh
-- Generated on: 2025-07-07 09:25:10
-- Total statements for this schema: 47
--
-- Source files:
--   ./sql/create_table_sql/create_EHR.sql
--   ./sql/create_table_sql/create_address.sql
--   ./sql/create_table_sql/create_clinical_organization.sql
--   ./sql/create_table_sql/create_healthcarebrand.sql
--   ./sql/create_table_sql/create_identifier.sql
--   ./sql/create_table_sql/create_individual.sql
--   ./sql/create_table_sql/create_interop_endpoint.sql
--   ./sql/create_table_sql/create_npi.sql
--   ./sql/create_table_sql/create_payer_data.sql
--   ./sql/create_table_sql/create_phone.sql
--   ./sql/create_table_sql/create_provider_taxonomy.sql
--   ./sql/create_table_sql/create_user_tables.sql


-- Source: ./sql/create_table_sql/create_address.sql
CREATE TABLE ndh.address (
    id SERIAL PRIMARY KEY,
    barcode_delivery_code VARCHAR(12),
    smarty_key VARCHAR(10),
    address_us_id INT NULL,
    address_international_id INT NULL,
    address_nonstandard_id INT NULL
);

-- Source: ./sql/create_table_sql/create_address.sql
CREATE TABLE ndh.address_us (
    id SERIAL PRIMARY KEY,
    address_id INT NOT NULL,
    input_id VARCHAR(36),
    input_index INT,
    candidate_index INT,
    addressee VARCHAR(64),
    delivery_line_1 VARCHAR(64),
    delivery_line_2 VARCHAR(64),
    last_line VARCHAR(64),
    delivery_point_barcode VARCHAR(12),
    
    -- Components
    urbanization VARCHAR(64),
    primary_number VARCHAR(30),
    street_name VARCHAR(64),
    street_predirection VARCHAR(16),
    street_postdirection VARCHAR(16),
    street_suffix VARCHAR(16),
    secondary_number VARCHAR(32),
    secondary_designator VARCHAR(16),
    extra_secondary_number VARCHAR(32),
    extra_secondary_designator VARCHAR(16),
    pmb_designator VARCHAR(16),
    pmb_number VARCHAR(16),
    city_name VARCHAR(64),
    default_city_name VARCHAR(64),
    state_abbreviation CHAR(2),
    zipcode CHAR(5),
    plus4_code VARCHAR(4),
    delivery_point CHAR(2),
    delivery_point_check_digit CHAR(1),
    
    -- Metadata
    record_type CHAR(1),
    zip_type VARCHAR(32),
    county_fips CHAR(5),
    county_name VARCHAR(64),
    ews_match CHAR(5),
    carrier_route CHAR(4),
    congressional_district CHAR(2),
    building_default_indicator CHAR(1),
    rdi VARCHAR(12),
    elot_sequence VARCHAR(4),
    elot_sort VARCHAR(4),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    coordinate_license INT,
    geo_precision VARCHAR(18),
    time_zone VARCHAR(48),
    utc_offset DECIMAL(4,2),
    dst CHAR(5),
    
    -- Analysis
    dpv_match_code VARCHAR(1),
    dpv_footnotes VARCHAR(32),
    dpv_cmra VARCHAR(1),
    dpv_vacant VARCHAR(1),
    dpv_no_stat VARCHAR(1),
    active VARCHAR(1),
    footnotes VARCHAR(24),
    lacslink_code VARCHAR(2),
    lacslink_indicator VARCHAR(1),
    suitelink_match VARCHAR(5),
    enhanced_match VARCHAR(64)
);

-- Source: ./sql/create_table_sql/create_address.sql
CREATE TABLE ndh.address_international (
    id SERIAL PRIMARY KEY,
    address_id INT NOT NULL,
    input_id VARCHAR(36),
    country VARCHAR(64),
    geocode VARCHAR(4),
    local_language VARCHAR(6),
    freeform VARCHAR(512),
    address1 VARCHAR(64),
    address2 VARCHAR(64),
    address3 VARCHAR(64),
    address4 VARCHAR(64),
    organization VARCHAR(64),
    locality VARCHAR(64),
    administrative_area VARCHAR(32),
    postal_code VARCHAR(16),
    
    -- Components
    administrative_area_iso2 VARCHAR(8),
    sub_administrative_area VARCHAR(64),
    country_iso_3 VARCHAR(3),
    premise VARCHAR(64),
    premise_number VARCHAR(64),
    thoroughfare VARCHAR(64),
    
    -- Metadata
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    geocode_precision VARCHAR(32),
    max_geocode_precision VARCHAR(32),
    address_format VARCHAR(128),
    
    -- Analysis
    verification_status VARCHAR(32),
    address_precision VARCHAR(32),
    max_address_precision VARCHAR(32)
);

-- Source: ./sql/create_table_sql/create_address.sql
CREATE TABLE ndh.address_nonstandard (
    id SERIAL PRIMARY KEY,
    address_id INT NOT NULL,
    input_id VARCHAR(36),
    input_index INT,
    candidate_index INT,
    addressee VARCHAR(64),
    delivery_line_1 VARCHAR(64),
    delivery_line_2 VARCHAR(64),
    last_line VARCHAR(64),
    
    -- Any additional fields specific to non-standard addresses
    address_type VARCHAR(32),
    address_format VARCHAR(128),
    raw_address TEXT,
    notes TEXT
);

-- Source: ./sql/create_table_sql/create_address.sql
CREATE TABLE ndh.AddressTypeLUT (
    id SERIAL PRIMARY KEY,
    address_type_description TEXT   NOT NULL,
    CONSTRAINT uc_AddressTypeLUT_address_type_description UNIQUE (
        address_type_description
    )
);

-- Source: ./sql/create_table_sql/create_address.sql
CREATE TABLE ndh.StateCodeLUT (
    id SERIAL PRIMARY KEY,
    state_code VARCHAR(100)   NOT NULL,
    state_name VARCHAR(100)   NOT NULL,
    CONSTRAINT uc_StateCodeLUT_state_code UNIQUE (
        state_code
    )
);

-- Source: ./sql/create_table_sql/create_address.sql
CREATE TABLE ndh.NPIAddress (
    id SERIAL PRIMARY KEY,
    NPI_id BIGINT   NOT NULL,
    AddressType_id INTEGER   NOT NULL,
    Address_id INT   NOT NULL
);

-- Source: ./sql/create_table_sql/create_clinical_organization.sql
CREATE TABLE ndh.ClinicalOrganization (
    id SERIAL PRIMARY KEY,
    ClinicalOrganization_legal_name VARCHAR(200)   NOT NULL,
    AuthorizedOfficial_Individual_id INT   NOT NULL,
    Organization_TIN VARCHAR(10)   DEFAULT NULL,
    Organization_VTIN VARCHAR(50) DEFAULT NULL,
    OrganizationGLIEF VARCHAR(300)  DEFAULT NULL,
    CONSTRAINT uc_Organization_Organization_VTIN UNIQUE (
        Organization_VTIN
    )
);

-- Source: ./sql/create_table_sql/create_clinical_organization.sql
CREATE TABLE ndh.ClinicalOrgnameTypeLUT (
    id SERIAL PRIMARY KEY,
    orgname_type_description TEXT   NOT NULL,
    source_file TEXT   NOT NULL,
    source_field TEXT   NOT NULL,
    CONSTRAINT uc_OrgnameTypeLUT_orgname_description UNIQUE (
        orgname_type_description
    )
);

-- Source: ./sql/create_table_sql/create_clinical_organization.sql
CREATE TABLE ndh.Orgname (
    id SERIAL PRIMARY KEY,
    ClinicalOrganization_id INT   NOT NULL,
    ClinicalOrganization_name VARCHAR(70)   NOT NULL,
    ClinicalOrgnameType_id INTEGER   NOT NULL
);

-- Source: ./sql/create_table_sql/create_EHR.sql
CREATE TABLE ndh.EHRToNPI (
    id SERIAL PRIMARY KEY,
    NPI_id BIGINT   NOT NULL,
    EHR_id INT   NOT NULL
);

-- Source: ./sql/create_table_sql/create_EHR.sql
CREATE TABLE ndh.EHR (
    id SERIAL PRIMARY KEY,
    -- Sourced from CHPL data here https://chpl.healthit.gov/
    CHPL_ID VARCHAR(200)   NOT NULL,
    bulk_endpoint_json_url VARCHAR(500) NULL
);

-- Source: ./sql/create_table_sql/create_healthcarebrand.sql
CREATE TABLE ndh.HealthcareBrand (
    id SERIAL PRIMARY KEY,
    HealthcareBrand_name VARCHAR(200)   NOT NULL,
    TrademarkSerialNumber VARCHAR(20)   NOT NULL
);

-- Source: ./sql/create_table_sql/create_healthcarebrand.sql
CREATE TABLE ndh.OrganizationToHealthcareBrand (
    id SERIAL PRIMARY KEY,
    HealthcareBrand_id INT   NOT NULL,
    Organization_id INT   NOT NULL
);

-- Source: ./sql/create_table_sql/create_identifier.sql
CREATE TABLE ndh.IdentifierTypeLUT (
    id SERIAL PRIMARY KEY,
    identifier_type_description TEXT   NOT NULL,
    CONSTRAINT uc_IdentifierTypeLUT_identifier_type_description UNIQUE (
        identifier_type_description
    )
);

-- Source: ./sql/create_table_sql/create_identifier.sql
CREATE TABLE ndh.NPIIdentifier (
    id SERIAL PRIMARY KEY,
    NPI_id BIGINT   NOT NULL,
    identifier VARCHAR(21)   NOT NULL,
    IdentifierType_id INTEGER   NOT NULL,
    state VARCHAR(3)   NOT NULL,
    issuer VARCHAR(81)   NOT NULL
);

-- Source: ./sql/create_table_sql/create_individual.sql
CREATE TABLE ndh.CredentialLUT (
    id SERIAL PRIMARY KEY,
    -- i.e. M.D.
    Credential_acronym VARCHAR(20)   NOT NULL,
    -- i.e. Medical Doctor
    Credential_name VARCHAR(100)   NOT NULL,
    -- for when there is only one source for the credential (unlike medical schools etc)
    Credential_source_url VARCHAR(250)   NOT NULL
);

-- Source: ./sql/create_table_sql/create_individual.sql
CREATE TABLE ndh.IndividualToCredential (
    id SERIAL PRIMARY KEY,
    Individual_id int   NOT NULL,
    Credential_id int   NOT NULL
);

-- Source: ./sql/create_table_sql/create_individual.sql
CREATE TABLE ndh.Individual (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(100)   NOT NULL,
    first_name VARCHAR(100)   NOT NULL,
    middle_name VARCHAR(21)   NOT NULL,
    name_prefix VARCHAR(6)   NOT NULL,
    name_suffix VARCHAR(6)   NOT NULL,
    email_address VARCHAR(200)   DEFAULT NULL,
    SSN VARCHAR(10)   DEFAULT NULL.
    sex_code CHAR(1)  DEFAULT NULL
);

-- Source: ./sql/create_table_sql/create_interop_endpoint.sql
CREATE TABLE ndh.NPIToEndpoint (
    id SERIAL PRIMARY KEY,
    NPI_id BIGINT   NOT NULL,
    Endpoint_id INT   NOT NULL
);

-- Source: ./sql/create_table_sql/create_interop_endpoint.sql
CREATE TABLE ndh.InteropEndpointTypeLUT (
    id SERIAL PRIMARY KEY,
    identifier_type_description TEXT   NOT NULL,
    CONSTRAINT uc_EndpointTypeLUT_identifier_type_description UNIQUE (
        identifier_type_description
    )
);

-- Source: ./sql/create_table_sql/create_interop_endpoint.sql
CREATE TABLE ndh.InteropEndpoint (
    id SERIAL PRIMARY KEY,
    -- for now only FHIR and Direct
    fhir_endpoint_url VARCHAR(500)   NOT NULL,
    -- endpoint NPPES file as endpoint_description
    endpoint_name VARCHAR(100)   NOT NULL,
    -- endpoint NPPES file as endpoint_comments
    endpoint_desc VARCHAR(100)   NOT NULL,
    EndpointAddress_id int   NOT NULL, -- this I am unsure about. It is specified in the FHIR standard, but perhaps it is ephemerial? What does it mean for a mutli-ONPI EHR endpoint to have 'an' address?
    InteropEndpointType_id int   NOT NULL
);

-- Source: ./sql/create_table_sql/create_interop_endpoint.sql
CREATE TABLE ndh.OrgToInteropEndpoint (
    id SERIAL PRIMARY KEY,
    Organization_id int   NOT NULL,
    InteropEndpoint_id int   NOT NULL
);

-- Source: ./sql/create_table_sql/create_npi.sql
CREATE TABLE ndh.NPI (
    id BIGINT PRIMARY KEY,
    npi BIGINT   NOT NULL,
    entity_type_code SMALLINT   NOT NULL,
    replacement_npi BIGINT  DEFAULT NULL,
    enumeration_date DATE  NOT NULL,
    last_update_date DATE   NOT NULL,
    deactivation_reason_code VARCHAR(3)   NOT NULL,
    deactivation_date DATE ,
    reactivation_date DATE ,
    certification_date DATE 
);

-- Source: ./sql/create_table_sql/create_npi.sql
CREATE TABLE ndh.NPI_to_Individual (
    id BIGINT  PRIMARY KEY,
    NPI_id BIGINT   NOT NULL UNIQUE,
    Individual_id INT   NOT NULL,
    is_sole_proprietor BOOLEAN   NOT NULL

);

-- Source: ./sql/create_table_sql/create_npi.sql
CREATE TABLE ndh.NPI_to_ClinicalOrganization (
    id BIGINT  PRIMARY KEY,
    NPI_id BIGINT   NOT NULL UNIQUE,
    ClinicalOrganization_id INT  DEFAULT NULL,
    PrimaryAuthorizedOfficial_Individual_id INT NOT NULL,
    Parent_NPI_id BIGINT DEFAULT NULL-- TODO shold this be its own intermediate table? With an is_primary boolean in it?
);

-- Source: ./sql/create_table_sql/create_payer_data.sql
CREATE TABLE ndh.PayerToInteropEndpoint (
    id SERIAL PRIMARY KEY,
    Payer_id int   NOT NULL,
    InteropEndpoint_id int   NOT NULL
);

-- Source: ./sql/create_table_sql/create_payer_data.sql
CREATE TABLE ndh.Payer (
    -- marketplace/network-puf.IssuerID
    id SERIAL PRIMARY KEY,
    -- marketplace/plan-attributes-puf.IssuerMarketPlaceMarketingName
    PayerName varchar   NOT NULL
);

-- Source: ./sql/create_table_sql/create_payer_data.sql
CREATE TABLE ndh.Plan (
    -- marketplace/plan-attributes-puf.PlanId
    id SERIAL PRIMARY KEY,
    Payer_id int   NOT NULL,
    MarketCoverage_id int   NOT NULL,
    -- marketplace/plan-attributes-puf.ServiceAreaId
    ServiceArea_id int   NOT NULL,
    -- marketplace/plan-attributes-puf.DentalOnlyPlan
    DentalOnlyPlan boolean   NOT NULL,
    -- marketplace/plan-attributes-puf.PlanMarketingName
    PlanMarketingName varchar   NOT NULL,
    -- marketplace/plan-attributes-puf.HIOSProductId
    HIOSProductID varchar   NOT NULL,
    PlanType_id int   NOT NULL,
    -- marketplace/plan-attributes-puf.IsNewPlan
    IsNewPlan boolean   NOT NULL
);

-- Source: ./sql/create_table_sql/create_payer_data.sql
CREATE TABLE ndh.PlanType (
    id SERIAL PRIMARY KEY,
    -- marketplace/plan-attributes-puf.PlanType
    PlanType varchar   NOT NULL
);

-- Source: ./sql/create_table_sql/create_payer_data.sql
CREATE TABLE ndh.MarketCoverage (
    id SERIAL PRIMARY KEY,
    -- marketplace/plan-attributes-puf.MarketCoverage
    MarketCoverage varchar   NOT NULL
);

-- Source: ./sql/create_table_sql/create_payer_data.sql
CREATE TABLE ndh.PlanNetworkToPlan (
    id SERIAL PRIMARY KEY,
    Plan_id int   NOT NULL,
    PlanNetwork_id int   NOT NULL
);

-- Source: ./sql/create_table_sql/create_payer_data.sql
CREATE TABLE ndh.PlanNetwork (
    -- marketplace/network-puf.NetworkID
    id SERIAL PRIMARY KEY,
    -- marketplace/network-puf.NetworkName
    PlanNetworkName varchar   NOT NULL,
    -- marketplace/network-puf.NetworkURL
    PlanNetworkURL varchar   NOT NULL
);

-- Source: ./sql/create_table_sql/create_payer_data.sql
CREATE TABLE ndh.ServiceArea (
    -- marketplace/plan-attributes-puf.ServiceAreaId
    id SERIAL PRIMARY KEY,
    -- marketplace/service-area-puf.ServiceAreaName
    ServiceAreaName varchar   NOT NULL,
    -- marketplace/service-area-puf.StateCode
    StateCode varchar   NOT NULL
    -- wishlist
    -- , service_area_shape GEOMETRY(MULTIPOLYGON, 4326)   NOT NULL -- enable with PostGIS turned on! 
);

-- Source: ./sql/create_table_sql/create_payer_data.sql
CREATE TABLE ndh.PlanNetworkToOrg (
    id SERIAL PRIMARY KEY,
    PlanNetwork_id int   NOT NULL,
    Organization_id int   NOT NULL
);

-- Source: ./sql/create_table_sql/create_phone.sql
CREATE TABLE ndh.PhoneTypeLUT (
    id SERIAL PRIMARY KEY,
    phone_type_description TEXT   NOT NULL,
    CONSTRAINT uc_PhoneTypeLUT_phone_type_description UNIQUE (
        phone_type_description
    )
);

-- Source: ./sql/create_table_sql/create_phone.sql
CREATE TABLE ndh.NPIToPhone (
    id SERIAL PRIMARY KEY,
    NPI_id BIGINT   NOT NULL,
    PhoneType_id INTEGER   NOT NULL,
    PhoneNumber_id INTEGER   NOT NULL,
    PhoneExtension_id INTEGER  NULL,
    is_fax BOOLEAN   NOT NULL
);

-- Source: ./sql/create_table_sql/create_phone.sql
Create TABLE ndh.PhoneNumber (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20)   NOT NULL,
    CONSTRAINT uc_PhoneNumber_phone_number UNIQUE (phone_number)
);

-- Source: ./sql/create_table_sql/create_phone.sql
Create TABLE ndh.PhoneExtension (
    id SERIAL PRIMARY KEY,
    phone_extension VARCHAR(10)   NOT NULL,
    CONSTRAINT uc_PhoneExtension_phone_extension UNIQUE (phone_extension)
);

-- Source: ./sql/create_table_sql/create_provider_taxonomy.sql
CREATE TABLE ndh.NUCCTaxonomyCode (
    id SERIAL PRIMARY KEY,
    ParentNUCCTaxonomyCode_id INT   NOT NULL,
    taxonomy_code VARCHAR(10)   NOT NULL,
    tax_grouping TEXT   NOT NULL,
    tax_classification TEXT   NOT NULL,
    tax_specialization TEXT   NOT NULL,
    tax_definition TEXT   NOT NULL,
    tax_notes TEXT   NOT NULL,
    tax_display_name TEXT   NOT NULL,
    tax_certifying_board_name TEXT   NOT NULL,
    tax_certifying_board_url TEXT   NOT NULL,
    CONSTRAINT uc_NUCCTaxonomyCode_taxonomy_code UNIQUE (
        taxonomy_code
    )
);

-- Source: ./sql/create_table_sql/create_provider_taxonomy.sql
CREATE TABLE ndh.NUCCTaxonomyCodePath (
    id SERIAL PRIMARY KEY,
    NUCCTaxonomyCodeDecendant_id INT   NOT NULL,
    NUCCTaxonomyCodeAncestor_id INT   NOT NULL
);

-- Source: ./sql/create_table_sql/create_provider_taxonomy.sql
CREATE TABLE ndh.NPITaxonomy (
    id SERIAL PRIMARY KEY,
    NPI_id BIGINT   NOT NULL,
    NUCCTaxonomyCode_id INT   NOT NULL,
    license_number VARCHAR(20)   NOT NULL,
    StateCode_id INTEGER   NOT NULL,
    is_primary BOOLEAN   NOT NULL,
    taxonomy_group VARCHAR(10)   NOT NULL
);

-- Source: ./sql/create_table_sql/create_provider_taxonomy.sql
CREATE TABLE ndh.MedicareProviderType (
    id SERIAL PRIMARY KEY,
    MedicareProviderType_name VARCHAR   NOT NULL
);

-- Source: ./sql/create_table_sql/create_provider_taxonomy.sql
CREATE TABLE ndh.NUCCMedicareProviderType (
    id SERIAL PRIMARY KEY,
    MedicareProviderType_id INT   NOT NULL,
    NUCCTaxonomyCode_id INT   NOT NULL
);

-- Source: ./sql/create_table_sql/create_user_tables.sql
CREATE TABLE ndh.User (
    id SERIAL PRIMARY KEY,
    Email varchar   NOT NULL,
    FirstName varchar   NOT NULL,
    LastName varchar   NOT NULL,
    IdentityVerified boolean   NOT NULL
);

-- Source: ./sql/create_table_sql/create_user_tables.sql
CREATE TABLE ndh.UserAccessRole (
    id SERIAL PRIMARY KEY,
    User_id INT   NOT NULL,
    Role_id INT   NOT NULL,
    NPI_id BIGINT   NOT NULL
);

-- Source: ./sql/create_table_sql/create_user_tables.sql
CREATE TABLE ndh."Role" (
    id SERIAL PRIMARY KEY,
    "Role" varchar(100)   NOT NULL
);
