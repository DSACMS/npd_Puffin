-- OverwriteThisOnNextCompile=True

CREATE DATABASE IF NOT EXISTS REPLACE_ME_DB_NAME;

DROP TABLE IF EXISTS REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME;

CREATE TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME (
    `compendium_hospital_id` VARCHAR(13),
    `ccn` VARCHAR(7),
    `hospital_name` VARCHAR(88),
    `hospital_street` VARCHAR(54),
    `hospital_city` VARCHAR(26),
    `hospital_state` VARCHAR(3),
    `hospital_zip` VARCHAR(6),
    `acutehosp_flag` VARCHAR(2),
    `health_sys_id` VARCHAR(12),
    `health_sys_name` VARCHAR(56),
    `health_sys_city` VARCHAR(21),
    `health_sys_state` VARCHAR(3),
    `corp_parent_id` VARCHAR(9),
    `corp_parent_name` VARCHAR(73),
    `corp_parent_type` VARCHAR(34),
    `hos_beds` VARCHAR(5),
    `hos_dsch` VARCHAR(7),
    `hos_res` VARCHAR(8),
    `hos_children` VARCHAR(2),
    `hos_majteach` VARCHAR(2),
    `hos_vmajteach` VARCHAR(2),
    `hos_teachint` VARCHAR(13),
    `hos_highdpp` VARCHAR(2),
    `hos_ucburden` VARCHAR(13),
    `hos_highuc` VARCHAR(2),
    `hos_ownership` VARCHAR(2),
    `hos_net_revenue` VARCHAR(11),
    `hos_total_revenue` VARCHAR(12)
);