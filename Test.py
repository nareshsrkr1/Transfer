DECLARE @PageNumber INT = 1;  -- Current page number
DECLARE @PageSize INT = 50;  -- Number of records per page

-- Fetch active columns dynamically from config or define explicitly
DECLARE @OrderByColumns NVARCHAR(MAX) = 'column1, column2, column3';  -- Replace with actual column names

WITH PaginatedResults AS (
    SELECT 
        d.*,
        o.exit_strategy_new AS overridden_exit_strategy,
        o.business_input_exit_strategy_new AS business_input_for_exit_strategy,
        o.exit_phase_new AS overridden_exit_phase,
        o.business_input_exit_phase_new AS business_input_for_exit_phase,
        o.exit_period_new AS overridden_exit_period,
        o.business_input_exit_period_new AS business_input_for_exit_period,
        o.last_updated_by,
        o.last_updated_on,
        ROW_NUMBER() OVER (
            ORDER BY 
                CASE WHEN @OrderByColumns IS NOT NULL THEN 
                    HASHBYTES('SHA2_256', CONCAT_WS('|', column1, column2, column3)) -- Active columns as tie-breakers
                ELSE NULL END
        ) AS row_num
    FROM 
        default_table AS d
    LEFT JOIN 
        override_json_table AS o
    ON 
        HASHBYTES('SHA2_256', 
            (SELECT CONCAT_WS('|', column1, column2, column3) 
             FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
        ) = o.segment_hash_id
)
SELECT * 
FROM PaginatedResults
WHERE row_num > (@PageNumber - 1) * @PageSize
  AND row_num <= @PageNumber * @PageSize;
