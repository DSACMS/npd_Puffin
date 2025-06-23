LOAD DATA LOCAL INFILE 'REPLACE_ME_CSV_FULL_PATH'
INTO TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    @NPI, @Endpoint_Type, @Endpoint_Type_Description, @Endpoint, @Affiliation, @Endpoint_Description, @Affiliation_Legal_Business_Name, @Use_Code, @Use_Description, @Other_Use_Description, @Content_Type, @Content_Description, @Other_Content_Description, @Affiliation_Address_Line_One, @Affiliation_Address_Line_Two, @Affiliation_Address_City, @Affiliation_Address_State, @Affiliation_Address_Country, @Affiliation_Address_Postal_Code
)
SET
    `NPI` = NULLIF(@NPI, ''),
    `Endpoint_Type` = NULLIF(@Endpoint_Type, ''),
    `Endpoint_Type_Description` = NULLIF(@Endpoint_Type_Description, ''),
    `Endpoint` = NULLIF(@Endpoint, ''),
    `Affiliation` = NULLIF(@Affiliation, ''),
    `Endpoint_Description` = NULLIF(@Endpoint_Description, ''),
    `Affiliation_Legal_Business_Name` = NULLIF(@Affiliation_Legal_Business_Name, ''),
    `Use_Code` = NULLIF(@Use_Code, ''),
    `Use_Description` = NULLIF(@Use_Description, ''),
    `Other_Use_Description` = NULLIF(@Other_Use_Description, ''),
    `Content_Type` = NULLIF(@Content_Type, ''),
    `Content_Description` = NULLIF(@Content_Description, ''),
    `Other_Content_Description` = NULLIF(@Other_Content_Description, ''),
    `Affiliation_Address_Line_One` = NULLIF(@Affiliation_Address_Line_One, ''),
    `Affiliation_Address_Line_Two` = NULLIF(@Affiliation_Address_Line_Two, ''),
    `Affiliation_Address_City` = NULLIF(@Affiliation_Address_City, ''),
    `Affiliation_Address_State` = NULLIF(@Affiliation_Address_State, ''),
    `Affiliation_Address_Country` = NULLIF(@Affiliation_Address_Country, ''),
    `Affiliation_Address_Postal_Code` = NULLIF(@Affiliation_Address_Postal_Code, '')
;