CREATE TABLE override_json_table (
    segment_json NVARCHAR(MAX),         -- JSON representation of the segments
    segment_hash_id NVARCHAR(255),     -- Hash ID for the segment JSON
    exit_strategy NVARCHAR(255),       -- Default exit strategy
    exit_strategy_new NVARCHAR(255),   -- Updated exit strategy
    business_input_exit_strategy_new NVARCHAR(255), -- User input for exit strategy
    exit_phase NVARCHAR(255),          -- Default exit phase
    exit_phase_new NVARCHAR(255),      -- Updated exit phase
    business_input_exit_phase_new NVARCHAR(255), -- User input for exit phase
    exit_period NVARCHAR(255),         -- Default exit period
    exit_period_new NVARCHAR(255),     -- Updated exit period
    business_input_exit_period_new NVARCHAR(255), -- User input for exit period
    last_updated_by NVARCHAR(255),     -- User who made the change
    last_updated_on DATETIME           -- Timestamp of the change
);


    -- Step 1: Insert data from the existing wpd table to the new override_json_table
INSERT INTO override_json_table (
    segment_json, 
    segment_hash_id, 
    exit_strategy, 
    exit_strategy_new, 
    business_input_exit_strategy_new, 
    exit_phase, 
    exit_phase_new, 
    business_input_exit_phase_new, 
    exit_period, 
    exit_period_new, 
    business_input_exit_period_new, 
    last_updated_by, 
    last_updated_on
)
SELECT 
    -- Generate JSON for active segments
    (SELECT 
         record_entity_name AS record_entity_name,
         maturity_bucket AS maturity_bucket,
         local_currency AS local_currency,
         product_liquidity AS product_liquidity,
         transaction_type AS transaction_type,
         collateralization AS collateralization,
         counterparty_type AS counterparty_type
     FOR JSON PATH, WITHOUT_ARRAY_WRAPPER) AS segment_json,

    -- Generate hash ID for the JSON object
    HASHBYTES('SHA2_256', 
        (SELECT 
            record_entity_name AS record_entity_name,
            maturity_bucket AS maturity_bucket,
            local_currency AS local_currency,
            product_liquidity AS product_liquidity,
            transaction_type AS transaction_type,
            collateralization AS collateralization,
            counterparty_type AS counterparty_type
        FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)) AS segment_hash_id,

    -- Default values from the wpd table
    wpd.exit_strategy AS exit_strategy,
    wpd.exit_strategy_new AS exit_strategy_new,
    wpd.business_input AS business_input_exit_strategy_new,
    wpd.exit_phase AS exit_phase,
    wpd.exit_phase_new AS exit_phase_new,
    wpd.business_input_exit_phase_new AS business_input_exit_phase_new,
    NULL AS exit_period,          -- Default exit period (if not available in wpd)
    wpd.exit_period_new AS exit_period_new,
    NULL AS business_input_exit_period_new, -- Business input for exit period (if not available in wpd)

    -- Metadata
    wpd.last_updated_by,
    wpd.last_updated_on
FROM wpd
WHERE 
    wpd.exit_strategy_new IS NOT NULL 
    OR wpd.exit_phase_new IS NOT NULL 
    OR wpd.exit_period_new IS NOT NULL;
