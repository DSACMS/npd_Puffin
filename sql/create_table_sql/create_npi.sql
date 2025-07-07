
-- These tables capture the dual-database nature of the NPI database which is so foundational to medical claims processing that we will have to keep it. 
-- We want to support more sophisticated modeling of clinical organizations 


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

CREATE TABLE ndh.NPI_to_Individual (
    id BIGINT  PRIMARY KEY,
    NPI_id INT   NOT NULL,
    Individual_id INT   NOT NULL,
    is_sole_proprietor BOOLEAN   NOT NULL,
    sex_code CHAR(1)   NOT NULL
);

CREATE TABLE ndh.NPI_to_ClinicalOrganization (
    id BIGINT  PRIMARY KEY,
    NPI_id BIGINT   NOT NULL,
    ClinicalOrganization_id INT  DEFAULT NULL,
    PrimaryAuthorizedOfficial_Individual_id INT NOT NULL,
    Parent_NPI_id BIGINT DEFAULT NULL-- TODO shold this be its own intermediate table? With an is_primary boolean in it?
);
