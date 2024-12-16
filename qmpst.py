SELECT 
    COUNT(*) as total_records,
    COUNT(INTENDED_DAYS_SUPPLY_QTY) as non_null_days_supply,
    COUNT(PATIENT_AGE_NBR) as non_null_patient_age,
    COUNT(FILL_STATUS_CD) as non_null_fill_status,
    COUNT(NDC) as non_null_ndc,
    COUNT(GCN_SEQUENCE_NBR) as non_null_gcn
FROM PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_DRUG;
