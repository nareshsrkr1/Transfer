UPDATE unfd_positions_dt u
SET ccr_rwa = CASE 
    -- First priority: Match legTransactionId
    WHEN s1.stdAllocatedRwa IS NOT NULL THEN s1.stdAllocatedRwa  
    -- Second priority: Match transactionId and sum stdAllocatedRwa
    WHEN s2.sum_stdAllocatedRwa IS NOT NULL THEN s2.sum_stdAllocatedRwa  
    -- No match: Keep ccr_rwa unchanged
    ELSE u.ccr_rwa  
END, 
rwa_sacr_flag = CASE 
    -- If legTransactionId or transactionId match, set flag to 'Y'
    WHEN s1.stdAllocatedRwa IS NOT NULL OR s2.sum_stdAllocatedRwa IS NOT NULL THEN 'Y'  
    -- No match: Set flag to 'N'
    ELSE 'N'  
END
FROM unfd_positions_dt u  
LEFT JOIN sacr_rwa_ead_data s1 ON u.transaction_id_facs = s1.legTransactionId  -- Direct match  
LEFT JOIN (  
    SELECT transactionId, SUM(stdAllocatedRwa) AS sum_stdAllocatedRwa  
    FROM sacr_rwa_ead_data  
    GROUP BY transactionId  
) s2 ON u.transaction_id_facs = s2.transactionId  -- Fallback match
