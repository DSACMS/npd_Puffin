LOAD DATA LOCAL INFILE 'REPLACE_ME_CSV_FULL_PATH'
INTO TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    @compendium_hospital_id, @ccn, @hospital_name, @hospital_street, @hospital_city, @hospital_state, @hospital_zip, @acutehosp_flag, @health_sys_id, @health_sys_name, @health_sys_city, @health_sys_state, @corp_parent_id, @corp_parent_name, @corp_parent_type, @hos_beds, @hos_dsch, @hos_res, @hos_children, @hos_majteach, @hos_vmajteach, @hos_teachint, @hos_highdpp, @hos_ucburden, @hos_highuc, @hos_ownership, @hos_net_revenue, @hos_total_revenue
)
SET
    `compendium_hospital_id` = NULLIF(@compendium_hospital_id, ''),
    `ccn` = NULLIF(@ccn, ''),
    `hospital_name` = NULLIF(@hospital_name, ''),
    `hospital_street` = NULLIF(@hospital_street, ''),
    `hospital_city` = NULLIF(@hospital_city, ''),
    `hospital_state` = NULLIF(@hospital_state, ''),
    `hospital_zip` = NULLIF(@hospital_zip, ''),
    `acutehosp_flag` = NULLIF(@acutehosp_flag, ''),
    `health_sys_id` = NULLIF(@health_sys_id, ''),
    `health_sys_name` = NULLIF(@health_sys_name, ''),
    `health_sys_city` = NULLIF(@health_sys_city, ''),
    `health_sys_state` = NULLIF(@health_sys_state, ''),
    `corp_parent_id` = NULLIF(@corp_parent_id, ''),
    `corp_parent_name` = NULLIF(@corp_parent_name, ''),
    `corp_parent_type` = NULLIF(@corp_parent_type, ''),
    `hos_beds` = NULLIF(@hos_beds, ''),
    `hos_dsch` = NULLIF(@hos_dsch, ''),
    `hos_res` = NULLIF(@hos_res, ''),
    `hos_children` = NULLIF(@hos_children, ''),
    `hos_majteach` = NULLIF(@hos_majteach, ''),
    `hos_vmajteach` = NULLIF(@hos_vmajteach, ''),
    `hos_teachint` = NULLIF(@hos_teachint, ''),
    `hos_highdpp` = NULLIF(@hos_highdpp, ''),
    `hos_ucburden` = NULLIF(@hos_ucburden, ''),
    `hos_highuc` = NULLIF(@hos_highuc, ''),
    `hos_ownership` = NULLIF(@hos_ownership, ''),
    `hos_net_revenue` = NULLIF(@hos_net_revenue, ''),
    `hos_total_revenue` = NULLIF(@hos_total_revenue, '')
;