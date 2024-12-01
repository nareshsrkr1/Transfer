-- Update unfd table with data from saccr based on legTransactionId or transactionId
UPDATE unfd_positions_dt AS unfd
SET 
    CCR_RWA = COALESCE(saccr_leg.stdAllocatedRwa, saccr_trans.stdAllocatedRwa),
    RWA_SACCR_FLAG = CASE 
        WHEN saccr_leg.stdAllocatedRwa IS NOT NULL OR saccr_trans.stdAllocatedRwa IS NOT NULL 
        THEN 'Y' 
        ELSE 'N' 
    END
FROM 
    saccr_rwa_ead_data saccr_leg
    FULL OUTER JOIN saccr_rwa_ead_data saccr_trans
    ON saccr_leg.transactionId = saccr_trans.transactionId
WHERE 
    unfd.Transaction_ID_FACS = saccr_leg.legTransactionId
    OR unfd.Transaction_ID_FACS = saccr_trans.transactionId;
