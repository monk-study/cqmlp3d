-- Step 4A: Check data after first join
DROP TABLE IF EXISTS PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_DRUG_DEBUG;
CREATE TABLE PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_DRUG_DEBUG AS (
    SELECT
        FILL.*,
        DR.GCN_SEQUENCE_NBR,
        DR.HIC3_CD,
        COUNT(*) OVER () as TOTAL_RECORDS,
        COUNT(FILL.INTENDED_DAYS_SUPPLY_QTY) OVER () as NON_NULL_DAYS_SUPPLY,
        COUNT(FILL.PATIENT_AGE_NBR) OVER () as NON_NULL_PATIENT_AGE,
        COUNT(FILL.FILL_STATUS_CD) OVER () as NON_NULL_FILL_STATUS,
        COUNT(DR.NDC) OVER () as NON_NULL_NDC_MATCHES
    FROM PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_FILL FILL
    LEFT JOIN CORE_RX.CURATED_PRODUCT.DRUG DR
        ON DR.NDC = FILL.NDC
);

-- Step 4B: Check data after second join
DROP TABLE IF EXISTS PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_DRUG_FINAL_DEBUG;
CREATE TABLE PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_DRUG_FINAL_DEBUG AS (
    SELECT
        BASE.*,
        DC.SEQ_NO as DRUG_HIST_SEQ_NO,
        COUNT(*) OVER () as TOTAL_RECORDS_AFTER_DC,
        COUNT(BASE.INTENDED_DAYS_SUPPLY_QTY) OVER () as NON_NULL_DAYS_SUPPLY_AFTER_DC,
        COUNT(BASE.PATIENT_AGE_NBR) OVER () as NON_NULL_PATIENT_AGE_AFTER_DC,
        COUNT(BASE.FILL_STATUS_CD) OVER () as NON_NULL_FILL_STATUS_AFTER_DC,
        COUNT(DC.SEQ_NO) OVER () as NON_NULL_DC_MATCHES
    FROM PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_DRUG_DEBUG BASE
    LEFT JOIN APP_RPHAI.CURATED_RPHAI.DRUG_CARD_JSON_HIST DC
        ON DC.GCN_SEQ_NO = BASE.GCN_SEQUENCE_NBR
        AND DC.LOAD_DATE = DATEADD('DAY', -1, BASE.CLAIM_DT)
);
