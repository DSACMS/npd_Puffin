--Sourced from CHPL data and Lantern data



-- I would love it if this could be EHR to ONPI, but there are sole pracitioners and other informal partnership arrangements that mean that there are individuals who have no ONPI
-- who are using an EHR that has a distinct endpoint. 

CREATE TABLE ndh.EHRToNPI (
    id SERIAL PRIMARY KEY,
    NPI_id INT   NOT NULL,
    EHR_id int   NOT NULL
);

CREATE TABLE ndh.EHR (
    id SERIAL PRIMARY KEY,
    -- Sourced from CHPL data here https://chpl.healthit.gov/
    CHPL_ID VARCHAR(200)   NOT NULL,
    bulk_endpoint_json_url VARCHAR(500) NULL
);
