-- Analyze NDC and GCN relationships
WITH DrugAnalysis AS (
    SELECT 
        COUNT(*) as total_records,
        COUNT(CASE WHEN NDC IS NOT NULL THEN 1 END) as non_null_ndc,
        COUNT(CASE WHEN GCN_SEQUENCE_NBR != -1 THEN 1 END) as valid_gcn,
        COUNT(CASE WHEN GCN_SEQUENCE_NBR = -1 THEN 1 END) as default_gcn,
        COUNT(INTENDED_DAYS_SUPPLY_QTY) as non_null_days_supply,
        COUNT(PATIENT_AGE_NBR) as non_null_patient_age,
        COUNT(FILL_STATUS_CD) as non_null_fill_status
    FROM PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_DRUG
)
SELECT *,
    (valid_gcn * 100.0 / total_records)::DECIMAL(5,2) as valid_gcn_percentage,
    (non_null_ndc * 100.0 / total_records)::DECIMAL(5,2) as valid_ndc_percentage
FROM DrugAnalysis;

-- Check for NDC distribution in original FILL table
SELECT 
    COUNT(*) as total_records,
    COUNT(NDC) as records_with_ndc,
    COUNT(DISTINCT NDC) as unique_ndcs
FROM PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_FILL;

-- Analyze NDC matching between FILL and DRUG tables
WITH NDC_Analysis AS (
    SELECT DISTINCT f.NDC
    FROM PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_FILL f
    WHERE f.NDC IS NOT NULL
)
SELECT 
    COUNT(*) as total_distinct_ndcs,
    COUNT(CASE WHEN d.NDC IS NOT NULL THEN 1 END) as matching_ndcs,
    COUNT(CASE WHEN d.NDC IS NULL THEN 1 END) as non_matching_ndcs
FROM NDC_Analysis na
LEFT JOIN CORE_RX.CURATED_PRODUCT.DRUG d 
    ON d.NDC = na.NDC;
