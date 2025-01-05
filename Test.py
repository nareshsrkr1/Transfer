-- Step 1: Expand Segments with Customer_Legal_Entity_Name
INSERT INTO wpd (hashid, segment_json, exit_strnew, exit_phase_new, business_input_new, business_exit_strategy)
SELECT 
    LOWER(CONVERT(VARCHAR(64), 
        HASHBYTES('SHA2_256', 
            (
                SELECT 
                    dt.Business_Name,
                    dt.Records_Entity_Name,
                    dt.DnTProduct_Type,
                    dt.DerivativeOrCash,
                    dt.Maturity_Bucket,
                    dt.Local_Currency,
                    dt.Transaction_Type,
                    dt.Collateralization,
                    dt.CounterParty_Type,
                    dt.Product_Liquidity,
                    dt.Banking_TradingFlag,
                    dt.Exit_Strategy_Default,
                    dt.Exit_Phase_Default,
                    dt.Business_Input_Default,
                    u.Customer_Legal_Entity_Name
                FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
            )
        )
    ), 2) AS hashid, -- New hashid for granular segment
    JSON_MODIFY(
        JSON_MODIFY(
            dt.segment_json, 
            '$.Customer_Legal_Entity_Name', 
            u.Customer_Legal_Entity_Name
        ), 
        '$.Business', 
        dt.Business_Name
    ) AS segment_json, -- Updated JSON with Customer_Legal_Entity_Name
    o.exit_strnew, -- Carry forward existing override for Exit_Strategy_New
    o.exit_phase_new, -- Carry forward existing override for Exit_Phase_New
    o.business_input_new, -- Carry forward existing override for Business_Input_New
    NULL AS business_exit_strategy -- Reset business override for user updates
FROM 
    windDownParams_Unfd_Default AS dt
JOIN 
    windDownParams_Override_JSON AS o
    ON dt.hashid = o.hashid -- Match existing segments
JOIN 
    unfd AS u
    ON dt.Business_Name = u.Business_Name 
       AND dt.Records_Entity_Name = u.Records_Entity_Name;
