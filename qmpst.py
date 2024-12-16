-- Analyze the original data source
SELECT 
    COUNT(*) as total_records,
    COUNT(NDC) as records_with_ndc,
    COUNT(CASE WHEN NDC IS NULL THEN 1 END) as records_without_ndc,
    COUNT(DISTINCT STORE_NBR) as unique_stores,
    COUNT(DISTINCT RX_NBR) as unique_prescriptions,
    COUNT(DISTINCT MESSAGE_ID) as unique_messages,
    -- Check rejection patterns
    COUNT(CASE WHEN ELIGIBILITY_YN = 1 THEN 1 END) as eligibility_rejections,
    COUNT(CASE WHEN NBA5_ATTEMPTED = 1 THEN 1 END) as nba5_attempts,
    -- Sample some common rejection codes
    COUNT(DISTINCT REJECT_CD_1) as unique_reject_codes,
    COUNT(CASE WHEN REJECT_CD_1 IS NOT NULL THEN 1 END) as records_with_rejections
FROM PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_FILL
GROUP BY ELIGIBILITY_YN
ORDER BY ELIGIBILITY_YN;

-- Sample some records without NDCs to understand patterns
SELECT 
    MESSAGE_ID,
    STORE_NBR,
    RX_NBR,
    FILL_NBR,
    NDC,
    REJECT_CD_1,
    REJECT_CD_2,
    CONCAT_MSG_TXT,
    NBA5_ATTEMPTED,
    ELIGIBILITY_YN
FROM PL_APP_RPHAI.RAW_RPHAI.NBA5_WITH_FILL
WHERE NDC IS NULL
    AND ELIGIBILITY_YN = 1  -- Focus on eligibility rejections
LIMIT 10;
