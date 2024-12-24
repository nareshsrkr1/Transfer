-- Step 1: Create JSON for active segments using FOR JSON PATH
WITH ActiveSegmentsJSON AS (
    SELECT 
        record_entity_name,
        maturity_bucket,
        local_currency,
        product_liquidity,
        transaction_type,
        collateralization,
        counterparty_type,
        -- Generate JSON manually using FOR JSON PATH
        (SELECT 
            record_entity_name AS record_entity_name,
            maturity_bucket AS maturity_bucket,
            local_currency AS local_currency,
            product_liquidity AS product_liquidity,
            transaction_type AS transaction_type,
            collateralization AS collateralization,
            counterparty_type AS counterparty_type
        FOR JSON PATH, WITHOUT_ARRAY_WRAPPER) AS segment_json,
        -- Generate a unique hash for the segment JSON
        HASHBYTES('SHA2_256', (
            SELECT 
                record_entity_name AS record_entity_name,
                maturity_bucket AS maturity_bucket,
                local_currency AS local_currency,
                product_liquidity AS product_liquidity,
                transaction_type AS transaction_type,
                collateralization AS collateralization,
                counterparty_type AS counterparty_type
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        )) AS segment_hash_id,
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
