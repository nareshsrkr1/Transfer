CREATE PROCEDURE ConstructHashID
AS
BEGIN
    -- Step 1: Declare variables and temporary tables
    DECLARE @ActiveColumns TABLE (ColumnName NVARCHAR(255));
    DECLARE @MappedColumns TABLE (UnfdColumn NVARCHAR(255), OverrideColumn NVARCHAR(255));
    DECLARE @FinalColumns TABLE (ColumnExpression NVARCHAR(MAX));
    DECLARE @ColumnList NVARCHAR(MAX);
    DECLARE @HashQuery NVARCHAR(MAX);

    -- Step 2: Get active columns from the config table
    INSERT INTO @ActiveColumns (ColumnName)
    SELECT DISTINCT ConfigColumnName
    FROM ConfigTable;

    -- Step 3: Remove 'bidoffspread' column from active columns
    DELETE FROM @ActiveColumns WHERE ColumnName = 'bidoffspread';

    -- Step 4: Map column names from `unfd_or_mapping` table
    INSERT INTO @MappedColumns (UnfdColumn, OverrideColumn)
    SELECT UnfdColumn, OverrideColumn
    FROM unfd_or_mapping
    WHERE UnfdColumn IN (SELECT ColumnName FROM @ActiveColumns);

    -- Step 5: Add unmapped active columns and create lowercase aliases for mapped ones
    INSERT INTO @FinalColumns (ColumnExpression)
    SELECT 
        CASE 
            WHEN m.OverrideColumn IS NOT NULL THEN 'LOWER(' + u.ColumnName + ') AS [' + LOWER(m.OverrideColumn) + ']' -- Alias mapped columns
            ELSE 'LOWER(' + u.ColumnName + ') AS [' + LOWER(u.ColumnName) + ']' -- Alias unmapped columns to lowercase
        END
    FROM @ActiveColumns u
    LEFT JOIN @MappedColumns m
        ON u.ColumnName = m.UnfdColumn;

    -- Step 6: Add `exit_strategy`, `exit_phase`, and `exit_period` as `business_input` if they don’t exist
    IF NOT EXISTS (SELECT 1 FROM @FinalColumns WHERE ColumnExpression LIKE '%exit_strategy%')
        INSERT INTO @FinalColumns (ColumnExpression) VALUES ('LOWER(exit_strategy) AS [exit_strategy]');
    IF NOT EXISTS (SELECT 1 FROM @FinalColumns WHERE ColumnExpression LIKE '%exit_phase%')
        INSERT INTO @FinalColumns (ColumnExpression) VALUES ('LOWER(exit_phase) AS [exit_phase]');
    IF NOT EXISTS (SELECT 1 FROM @FinalColumns WHERE ColumnExpression LIKE '%business_input%')
        INSERT INTO @FinalColumns (ColumnExpression) VALUES ('LOWER(exit_period) AS [business_input]');

    -- Step 7: Order columns explicitly for JSON structure
    SELECT @ColumnList = STRING_AGG(ColumnExpression, ', ')
    FROM @FinalColumns
    ORDER BY 
        CASE 
            WHEN ColumnExpression LIKE '%business_name%' THEN 1
            WHEN ColumnExpression LIKE '%records_entity_name%' THEN 2
            WHEN ColumnExpression LIKE '%dntproduct_type%' THEN 3
            WHEN ColumnExpression LIKE '%derivativeorcash%' THEN 4
            WHEN ColumnExpression LIKE '%maturity_bucket%' THEN 5
            WHEN ColumnExpression LIKE '%local_currency%' THEN 6
            WHEN ColumnExpression LIKE '%transaction_type%' THEN 7
            WHEN ColumnExpression LIKE '%collateralization%' THEN 8
            WHEN ColumnExpression LIKE '%counterparty_type%' THEN 9
            WHEN ColumnExpression LIKE '%product_liquidity%' THEN 10
            WHEN ColumnExpression LIKE '%bankingtradingflag%' THEN 11
            WHEN ColumnExpression LIKE '%exit_strategy%' THEN 12
            WHEN ColumnExpression LIKE '%exit_phase%' THEN 13
            WHEN ColumnExpression LIKE '%business_input%' THEN 14
            ELSE 15 -- Fallback for unmapped columns
        END;

    -- Step 8: Construct the hashid query dynamically
    SET @HashQuery = '
        SELECT LOWER(CONVERT(VARCHAR(64), 
            HASHBYTES(''SHA2_256'', 
                (SELECT ' + @ColumnList + ' 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
            ), 2)) AS segment_hash_id, *
        FROM unfd_positions;
    ';

    -- Step 9: Execute the query to generate the hashid
    EXEC sp_executesql @HashQuery;
END;
GO
