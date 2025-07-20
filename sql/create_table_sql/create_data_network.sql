-- elements needed to power a homepage list of data networks

CREATE TABLE IF NOT EXISTS ndh.data_network (
    id SERIAL PRIMARY KEY,
    data_network_name varchar(100)   NOT NULL,
    data_network_blurb TEXT DEFAULT NULL,
    data_network_homepage_url varchar(500)   DEFAULT NULL,
    data_network_logo_url varchar(500)   DEFAULT NULL,
    is_medicare_aligned_network BOOLEAN,
    CONSTRAINT uc_data_network_name UNIQUE (
        data_network_name
    )        
);

CREATE TABLE IF NOT EXISTS ndh.npi_data_network (
    id SERIAL PRIMARY KEY,
    npi_id BIGINT   NOT NULL,
    data_network_id INT   NOT NULL
);


CREATE TABLE IF NOT EXISTS ndh.data_network_interop_endpoint (
    data_network_id INT,
    interop_endpoint_id INT
);

-- Example Data (do not represent actual commitments at this time. )

-- Athenahealth
INSERT INTO ndh.data_network(data_network_name, data_network_blurb, data_network_homepage_url, is_medicare_aligned_network)
VALUES ('Athenahealth', 'Cloud-Based Healthcare Products & Services | athenahealth', 'https://www.athenahealth.com/', TRUE);
INSERT INTO ndh.interop_endpoint(fhir_endpoint_url, endpoint_name, endpoint_desc)
VALUES ('https://docs.athenahealth.com/api/docs/fhir-apis', 'Athenahealth API', 'Athenahealth FHIR API');
INSERT INTO ndh.data_network_interop_endpoint(data_network_id, interop_endpoint_id)
VALUES (currval(pg_get_serial_sequence('ndh.data_network', 'id')), currval(pg_get_serial_sequence('ndh.interop_endpoint', 'id')));

-- eClinicalWorks
INSERT INTO ndh.data_network(data_network_name, data_network_blurb, data_network_homepage_url, is_medicare_aligned_network)
VALUES ('eClinicalWorks', 'A privately held leader in healthcare IT,', 'https://www.eclinicalworks.com/', TRUE);
INSERT INTO ndh.interop_endpoint(fhir_endpoint_url, endpoint_name, endpoint_desc)
VALUES ('https://fhir.eclinicalworks.com/ecwopendev/', 'eClinicalWorks API', 'eClinicalWorks FHIR API');
INSERT INTO ndh.data_network_interop_endpoint(data_network_id, interop_endpoint_id)
VALUES (currval(pg_get_serial_sequence('ndh.data_network', 'id')), currval(pg_get_serial_sequence('ndh.interop_endpoint', 'id')));

-- Surescripts
INSERT INTO ndh.data_network(data_network_name, data_network_blurb, data_network_homepage_url, is_medicare_aligned_network)
VALUES ('Surescripts', 'Trusted Health Intelligence Sharing', 'https://surescripts.com/', TRUE);
INSERT INTO ndh.interop_endpoint(fhir_endpoint_url, endpoint_name, endpoint_desc)
VALUES ('https://surescripts.com/insights/clinical-interoperability', 'Surescripts API', 'Surescripts Clinical Interoperability');
INSERT INTO ndh.data_network_interop_endpoint(data_network_id, interop_endpoint_id)
VALUES (currval(pg_get_serial_sequence('ndh.data_network', 'id')), currval(pg_get_serial_sequence('ndh.interop_endpoint', 'id')));
