
CREATE INDEX endpoint_file_NPI_index
    on REPLACE_ME_DATABASE_NAME.REPLACE_ME_TABLE_NAME (npi);

ALTER TABLE REPLACE_ME_DATABASE_NAME.REPLACE_ME_TABLE_NAME
    ADD CONSTRAINT endpoint_file_pk
        PRIMARY KEY (endpoint_type, endpoint_type_description, npi, "endpoint");

