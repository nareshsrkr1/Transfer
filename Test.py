WITH unifiedPositions AS (
    SELECT 
        Business_Name,
        Records_Entity_Name,
        DnT_Product_Type,
        DerivativeorCash,
        Derivative_Transaction_Channel,
        CounterParty_Type,
        currency_DT AS Local_Currency,
        Collateralization,
        Maturity_Bucket,
        Exit_Strategy AS Exit_Strategy_Default,
        Exit_Phase AS Exit_phase_Default,
        Exit_Period AS Total_Exit_Period_Months,
        SUM(CAST(Current_Position_Netted_MTM_Value_USD AS FLOAT)) AS NPV,
        SUM(ISNULL(CAST(Notional_USD AS FLOAT), 0)) AS Notional,
        BankingTradingFlag,
        COUNT(Transaction_ID_FACS) AS Trade_count,
        'Segment' AS ParamType,
        -- Calculate % of total trade count
        CAST(
            COUNT(Transaction_ID_FACS) * 100.0 / 
            SUM(COUNT(Transaction_ID_FACS)) OVER (PARTITION BY Business_Name) 
            AS VARCHAR
        ) + '%' AS TotalTrade_pct,
        -- Generate Product Liquidity
        CASE 
            WHEN Derivative_Transaction_Channel = 'OTC' THEN 
                Derivative_Transaction_Channel + ' ' + ISNULL(Collateralization, '')
            ELSE 
                Derivative_Transaction_Channel 
        END AS Product_Liquidity
    FROM UNFD_POSITIONS_DT
    GROUP BY
        Business_Name,
        Records_Entity_Name,
        DnT_Product_Type,
        DerivativeorCash,
        Derivative_Transaction_Channel,
        CounterParty_Type,
        currency_DT,
        Collateralization,
        Maturity_Bucket,
        Exit_Strategy,
        Exit_Phase,
        Exit_Period,
        BankingTradingFlag
)
SELECT 
    up.ParamType, 
    up.Business_Name,
    up.Records_Entity_Name,
    up.DerivativeorCash,
    up.DnT_Product_Type,
    up.Maturity_Bucket,
    up.Local_Currency,
    COALESCE(wpd.Transaction_Type, up.Derivative_Transaction_Channel) AS Transaction_Type,
    up.Collateralization,
    COALESCE(wpd.CounterParty_Type, up.CounterParty_Type) AS CounterParty_Type,
    up.Product_Liquidity,
    up.Trade_count,
    up.TotalTrade_pct,
    up.Notional,
    up.NPV,
    up.Exit_Strategy_Default,
    COALESCE(wpd.Exit_Strategy, up.Exit_Strategy_Default) AS Exit_Strategy_Final,
    wpd.Exit_Strategy_BusinessOverride AS Exit_Strategy_Override,
    up.Exit_phase_Default,
    COALESCE(wpd.Exit_phase, up.Exit_phase_Default) AS Exit_phase_Final,
    wpd.Exit_phase_BusinessOverride AS Exit_phase_Override,
    wpd.Business_Input AS Business_Input_new,
    wpd.Business_Input_BusinessOverride AS Business_Input_Override,
    up.Total_Exit_Period_Months,
    wpd.RunID,
    wpd.LastUpdatedBy,
    wpd.LastUpdatedOn,
    wpd.HashID,
    wpd.SegmentationID
FROM unifiedPositions up
LEFT JOIN windDownParams_Override wpd
    ON up.Business_Name = wpd.Business_Name
    AND up.Records_Entity_Name = wpd.Records_Entity_Name
    AND up.DnT_Product_Type = wpd.DnTProduct_Type
    AND up.DerivativeorCash = wpd.DerivativeorCash
    AND up.Maturity_Bucket = wpd.Maturity_Bucket
    AND up.Local_Currency = wpd.Local_Currency
    AND up.Collateralization = wpd.Collateralization
    AND up.Product_Liquidity = wpd.Product_Liquidity
    AND up.BankingTradingFlag = wpd.BankingTradingFlag
WHERE up.Business_Name = 'CMBS Trading';
