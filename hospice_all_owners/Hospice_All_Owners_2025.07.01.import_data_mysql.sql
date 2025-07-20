LOAD DATA LOCAL INFILE 'REPLACE_ME_CSV_FULL_PATH'
INTO TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    @enrollment_id, @associate_id, @organization_name, @associate_id_owner, @type_owner, @role_code_owner, @role_text_owner, @association_date_owner, @first_name_owner, @middle_name_owner, @last_name_owner, @title_owner, @organization_name_owner, @doing_business_as_name_owner, @address_line_1_owner, @address_line_2_owner, @city_owner, @state_owner, @zip_code_owner, @percentage_ownership, @created_for_acquisition_owner, @corporation_owner, @llc_owner, @medical_provider_supplier_owner, @management_services_company_owner, @medical_staffing_company_owner, @holding_company_owner, @investment_firm_owner, @financial_institution_owner, @consulting_firm_owner, @for_profit_owner, @non_profit_owner, @private_equity_company_owner, @reit_owner, @chain_home_office_owner, @other_type_owner, @other_type_text_owner, @owned_by_another_org_or_ind_owner
)
SET
    `enrollment_id` = NULLIF(@enrollment_id, ''),
    `associate_id` = NULLIF(@associate_id, ''),
    `organization_name` = NULLIF(@organization_name, ''),
    `associate_id_owner` = NULLIF(@associate_id_owner, ''),
    `type_owner` = NULLIF(@type_owner, ''),
    `role_code_owner` = NULLIF(@role_code_owner, ''),
    `role_text_owner` = NULLIF(@role_text_owner, ''),
    `association_date_owner` = NULLIF(@association_date_owner, ''),
    `first_name_owner` = NULLIF(@first_name_owner, ''),
    `middle_name_owner` = NULLIF(@middle_name_owner, ''),
    `last_name_owner` = NULLIF(@last_name_owner, ''),
    `title_owner` = NULLIF(@title_owner, ''),
    `organization_name_owner` = NULLIF(@organization_name_owner, ''),
    `doing_business_as_name_owner` = NULLIF(@doing_business_as_name_owner, ''),
    `address_line_1_owner` = NULLIF(@address_line_1_owner, ''),
    `address_line_2_owner` = NULLIF(@address_line_2_owner, ''),
    `city_owner` = NULLIF(@city_owner, ''),
    `state_owner` = NULLIF(@state_owner, ''),
    `zip_code_owner` = NULLIF(@zip_code_owner, ''),
    `percentage_ownership` = NULLIF(@percentage_ownership, ''),
    `created_for_acquisition_owner` = NULLIF(@created_for_acquisition_owner, ''),
    `corporation_owner` = NULLIF(@corporation_owner, ''),
    `llc_owner` = NULLIF(@llc_owner, ''),
    `medical_provider_supplier_owner` = NULLIF(@medical_provider_supplier_owner, ''),
    `management_services_company_owner` = NULLIF(@management_services_company_owner, ''),
    `medical_staffing_company_owner` = NULLIF(@medical_staffing_company_owner, ''),
    `holding_company_owner` = NULLIF(@holding_company_owner, ''),
    `investment_firm_owner` = NULLIF(@investment_firm_owner, ''),
    `financial_institution_owner` = NULLIF(@financial_institution_owner, ''),
    `consulting_firm_owner` = NULLIF(@consulting_firm_owner, ''),
    `for_profit_owner` = NULLIF(@for_profit_owner, ''),
    `non_profit_owner` = NULLIF(@non_profit_owner, ''),
    `private_equity_company_owner` = NULLIF(@private_equity_company_owner, ''),
    `reit_owner` = NULLIF(@reit_owner, ''),
    `chain_home_office_owner` = NULLIF(@chain_home_office_owner, ''),
    `other_type_owner` = NULLIF(@other_type_owner, ''),
    `other_type_text_owner` = NULLIF(@other_type_text_owner, ''),
    `owned_by_another_org_or_ind_owner` = NULLIF(@owned_by_another_org_or_ind_owner, '')
;