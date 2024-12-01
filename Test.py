-- Update unfd table with data from saccr based on legTransactionId or transactionId
UPDATE unfd
SET 
    CCR_RWA = COALESCE(
        COALESCE(saccr_leg.stdAllocatedRwa, saccr_trans.stdAllocatedRwa), 
        unfd.CCR_RWA
    ),
    RWA_SACCR_FLAG = CASE 
        WHEN saccr_leg.stdAllocatedRwa IS NOT NULL OR saccr_trans.stdAllocatedRwa IS NOT NULL 
        THEN 'Y' 
        ELSE RWA_SACCR_FLAG -- Retain existing value
    END
FROM 
    unfd_positions_dt unfd
    LEFT JOIN saccr_rwa_ead_data saccr_leg
        ON unfd.Transaction_ID_FACS = saccr_leg.legTransactionId
    LEFT JOIN saccr_rwa_ead_data saccr_trans
        ON unfd.Transaction_ID_FACS = saccr_trans.transactionId;
