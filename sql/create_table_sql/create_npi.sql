
-- These tables capture the dual-database nature of the NPI database which is so foundational to medical claims processing that we will have to keep it. 
-- We want to support more sophisticated modeling of clinical organizations 


CREATE TABLE ndh.npi (
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

-- TODO should we rename these to IndividualNPI and OrganizationalNPI respectively. 
-- They are not many-to-many against NPI and each NPI only has one or the other. 
-- These names better 

CREATE TABLE ndh.individual_npi (
    id BIGINT  PRIMARY KEY,
    npi_id BIGINT   NOT NULL UNIQUE,
    individual_id INT   NOT NULL,
    is_sole_proprietor BOOLEAN   NOT NULL

);

CREATE TABLE ndh.organizational_npi (
    id BIGINT  PRIMARY KEY,
    npi_id BIGINT   NOT NULL UNIQUE,
    clinical_organization_id INT  DEFAULT NULL,
    primary_authorized_official_individual_id INT NOT NULL,
    parent_npi_id BIGINT DEFAULT NULL-- TODO shold this be its own intermediate table? With an is_primary boolean in it?
);
