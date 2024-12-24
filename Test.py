-- Step 1: Create JSON for active segments
WITH ActiveSegmentsJSON AS (
    SELECT 
        -- Create a JSON object for all static segments in the wpd table
        JSON_OBJECT(
            'record_entity_name', record_entity_name,
            'maturity_bucket', maturity_bucket,
            'local_currency', local_currency,
            'product_liquidity', product_liquidity,
            'transaction_type', transaction_type,
            'collateralization', collateralization,
            'counterparty_type', counterparty_type
        ) AS segment_json,
        -- Generate a unique hash for the segment JSON
        HASHBYTES('SHA2_256', 
            JSON_OBJECT(
                'record_entity_name', record_entity_name,
                'maturity_bucket', maturity_bucket,
                'local_currency', local_currency,
                'product_liquidity', product_liquidity,
                'transaction_type', transaction_type,
                'collateralization', collateralization,
                'counterparty_type', counterparty_type
            )
        ) AS segment_hash_id,
        exit_strategy_new,
        business_Input AS exit_phase_new,
        NULL AS exit_period_new, -- Assuming this field isn't available in wpd
        last_updated_by,
        last_updated_on
    FROM wpd
    WHERE 
        exit_strategy_new IS NOT NULL 
        OR business_Input IS NOT NULL
)

-- Step 2: Insert the JSON and overrides into the override_json_table
INSERT INTO override_json_table (
    segment_json,
    segment_hash_id,
    exit_strategy_new,
    exit_phase_new,
    exit_period_new,
    last_updated_by,
    last_updated_on
)
SELECT 
    segment_json,
    CAST(segment_hash_id AS VARCHAR(255)),
    exit_strategy_new,
    exit_phase_new,
    exit_period_new,
    last_updated_by,
    last_updated_on
FROM ActiveSegmentsJSON;
