LOAD DATA LOCAL INFILE 'REPLACE_ME_CSV_FULL_PATH'
INTO TABLE REPLACE_ME_DB_NAME.REPLACE_ME_TABLE_NAME
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    @health_sys_id, @health_sys_name, @health_sys_city, @health_sys_state, @in_onekey, @in_aha, @onekey_id, @aha_sysid, @total_mds, @prim_care_mds, @total_nps, @total_pas, @grp_cnt, @grp_cnt_restricted, @hosp_cnt, @acutehosp_cnt, @nh_cnt, @nh_cnt_restricted, @hhco_cnt, @hhco_cnt_restricted, @sys_multistate, @sys_beds, @sys_dsch, @sys_res, @deg_children, @sys_incl_majteachhosp, @sys_incl_vmajteachhosp, @sys_teachint, @sys_incl_highdpphosp, @sys_highucburden, @sys_incl_highuchosp, @sys_anyins_product, @sys_mcare_adv, @sys_mcaid_mngcare, @sys_healthins_mktplc, @sys_ownership, @hos_net_revenue, @hos_total_revenue
)
SET
    `health_sys_id` = NULLIF(@health_sys_id, ''),
    `health_sys_name` = NULLIF(@health_sys_name, ''),
    `health_sys_city` = NULLIF(@health_sys_city, ''),
    `health_sys_state` = NULLIF(@health_sys_state, ''),
    `in_onekey` = NULLIF(@in_onekey, ''),
    `in_aha` = NULLIF(@in_aha, ''),
    `onekey_id` = NULLIF(@onekey_id, ''),
    `aha_sysid` = NULLIF(@aha_sysid, ''),
    `total_mds` = NULLIF(@total_mds, ''),
    `prim_care_mds` = NULLIF(@prim_care_mds, ''),
    `total_nps` = NULLIF(@total_nps, ''),
    `total_pas` = NULLIF(@total_pas, ''),
    `grp_cnt` = NULLIF(@grp_cnt, ''),
    `grp_cnt_restricted` = NULLIF(@grp_cnt_restricted, ''),
    `hosp_cnt` = NULLIF(@hosp_cnt, ''),
    `acutehosp_cnt` = NULLIF(@acutehosp_cnt, ''),
    `nh_cnt` = NULLIF(@nh_cnt, ''),
    `nh_cnt_restricted` = NULLIF(@nh_cnt_restricted, ''),
    `hhco_cnt` = NULLIF(@hhco_cnt, ''),
    `hhco_cnt_restricted` = NULLIF(@hhco_cnt_restricted, ''),
    `sys_multistate` = NULLIF(@sys_multistate, ''),
    `sys_beds` = NULLIF(@sys_beds, ''),
    `sys_dsch` = NULLIF(@sys_dsch, ''),
    `sys_res` = NULLIF(@sys_res, ''),
    `deg_children` = NULLIF(@deg_children, ''),
    `sys_incl_majteachhosp` = NULLIF(@sys_incl_majteachhosp, ''),
    `sys_incl_vmajteachhosp` = NULLIF(@sys_incl_vmajteachhosp, ''),
    `sys_teachint` = NULLIF(@sys_teachint, ''),
    `sys_incl_highdpphosp` = NULLIF(@sys_incl_highdpphosp, ''),
    `sys_highucburden` = NULLIF(@sys_highucburden, ''),
    `sys_incl_highuchosp` = NULLIF(@sys_incl_highuchosp, ''),
    `sys_anyins_product` = NULLIF(@sys_anyins_product, ''),
    `sys_mcare_adv` = NULLIF(@sys_mcare_adv, ''),
    `sys_mcaid_mngcare` = NULLIF(@sys_mcaid_mngcare, ''),
    `sys_healthins_mktplc` = NULLIF(@sys_healthins_mktplc, ''),
    `sys_ownership` = NULLIF(@sys_ownership, ''),
    `hos_net_revenue` = NULLIF(@hos_net_revenue, ''),
    `hos_total_revenue` = NULLIF(@hos_total_revenue, '')
;