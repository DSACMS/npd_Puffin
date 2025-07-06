


CREATE TABLE ndh.NPIToEndpoint (
    id SERIAL PRIMARY KEY,
    NPI_id BIGINT   NOT NULL,
    Endpoint_id INT   NOT NULL
);


-- these will most obviously include "Payer", "EHR", but could eventually run the gamut "PHR", "Public Health", "HIE", "Patient Registry", etc etc.


CREATE TABLE ndh.InteropEndpointTypeLUT (
    id SERIAL PRIMARY KEY,
    identifier_type_description TEXT   NOT NULL,
    CONSTRAINT uc_EndpointTypeLUT_identifier_type_description UNIQUE (
        identifier_type_description
    )
);




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

CREATE TABLE ndh.OrgToInteropEndpoint (
    id SERIAL PRIMARY KEY,
    Organization_id int   NOT NULL,
    InteropEndpoint_id int   NOT NULL
);
