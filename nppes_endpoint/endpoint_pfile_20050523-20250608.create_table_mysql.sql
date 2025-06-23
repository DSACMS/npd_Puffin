CREATE DATABASE IF NOT EXISTS REPLACE_ME_DB_NAME;

DROP TABLE IF EXISTS REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME;

CREATE TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME (
    `NPI` VARCHAR(11),
    `Endpoint_Type` VARCHAR(8),
    `Endpoint_Type_Description` VARCHAR(25),
    `Endpoint` VARCHAR(1001),
    `Affiliation` VARCHAR(2),
    `Endpoint_Description` VARCHAR(676),
    `Affiliation_Legal_Business_Name` VARCHAR(71),
    `Use_Code` VARCHAR(7),
    `Use_Description` VARCHAR(34),
    `Other_Use_Description` VARCHAR(188),
    `Content_Type` VARCHAR(6),
    `Content_Description` VARCHAR(6),
    `Other_Content_Description` VARCHAR(201),
    `Affiliation_Address_Line_One` VARCHAR(56),
    `Affiliation_Address_Line_Two` VARCHAR(56),
    `Affiliation_Address_City` VARCHAR(32),
    `Affiliation_Address_State` VARCHAR(26),
    `Affiliation_Address_Country` VARCHAR(3),
    `Affiliation_Address_Postal_Code` VARCHAR(14)
);