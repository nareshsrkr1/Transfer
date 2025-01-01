CREATE PROCEDURE ConstructHashID
AS
BEGIN
    -- Step 1: Declare variables and temporary tables
    DECLARE @ActiveColumns TABLE (ColumnName NVARCHAR(255));
    DECLARE @MappedColumns TABLE (UnfdColumn NVARCHAR(255), OverrideColumn NVARCHAR(255));
    DECLARE @FinalColumns TABLE (ColumnExpression NVARCHAR(MAX), SortOrder INT);
    DECLARE @OrderedColumnList NVARCHAR(MAX) = '
        business_name, 
        records_entity_name, 
        dntproduct_type, 
        derivativeorcash, 
        maturity_bucket, 
        local_currency, 
        transaction_type, 
        collateralization, 
        counterparty_type, 
        product_liquidity, 
        bankingtradingflag, 
        exit_strategy, 
        exit_phase, 
        business_input
    ';
    DECLARE @ColumnList NVARCHAR(MAX);
    DECLARE @HashQuery NVARCHAR(MAX);

    -- Step 2: Get active columns from the config table
    INSERT INTO @ActiveColumns (ColumnName)
    SELECT DISTINCT ConfigColumnName
    FROM ConfigTable;

    -- Step 3: Remove 'bidoffspread' column from active columns
    DELETE FROM @ActiveColumns WHERE ColumnName = 'bidoffspread';

    -- Step 4: Map column names using the unfd_or_mapping table
    INSERT INTO @MappedColumns (UnfdColumn, OverrideColumn)
    SELECT UnfdColumn, OverrideColumn
    FROM unfd_or_mapping
    WHERE UnfdColumn IN (SELECT ColumnName FROM @ActiveColumns);

    -- Step 5: Add alias columns to the final list
    INSERT INTO @FinalColumns (ColumnExpression, SortOrder)
    SELECT 
        CASE 
            WHEN m.OverrideColumn IS NOT NULL THEN u.ColumnName + ' AS [' + m.OverrideColumn + ']'
            ELSE u.ColumnName
        END AS ColumnExpression,
        CHARINDEX(',' + LOWER(u.ColumnName) + ',', ',' + @OrderedColumnList + ',') AS SortOrder
    FROM @ActiveColumns u
    LEFT JOIN @MappedColumns m
        ON u.ColumnName = m.UnfdColumn;

    -- Step 6: Add static override columns if not already present
    IF NOT EXISTS (SELECT 1 FROM @FinalColumns WHERE ColumnExpression LIKE '%exit_strategy%')
        INSERT INTO @FinalColumns (ColumnExpression, SortOrder)
        VALUES ('exit_strategy AS [exit_strategy]', 
                CHARINDEX(',exit_strategy,', ',' + @OrderedColumnList + ','));
    IF NOT EXISTS (SELECT 1 FROM @FinalColumns WHERE ColumnExpression LIKE '%exit_phase%')
        INSERT INTO @FinalColumns (ColumnExpression, SortOrder)
        VALUES ('exit_phase AS [exit_phase]', 
                CHARINDEX(',exit_phase,', ',' + @OrderedColumnList + ','));
    IF NOT EXISTS (SELECT 1 FROM @FinalColumns WHERE ColumnExpression LIKE '%business_input%')
        INSERT INTO @FinalColumns (ColumnExpression, SortOrder)
        VALUES ('exit_period AS [business_input]', 
                CHARINDEX(',business_input,', ',' + @OrderedColumnList + ','));

    -- Step 7: Assign default sort order for unmatched columns
    UPDATE @FinalColumns
    SET SortOrder = ISNULL(SortOrder, 1000 + ROW_NUMBER() OVER (ORDER BY ColumnExpression))
    WHERE SortOrder IS NULL;

    -- Step 8: Order columns explicitly based on predefined list and unmatched columns
    SELECT @ColumnList = STRING_AGG(ColumnExpression, ', ')
    FROM @FinalColumns
    ORDER BY SortOrder;

    -- Step 9: Construct the hashid query dynamically
    SET @HashQuery = '
        SELECT LOWER(CONVERT(VARCHAR(64), 
            HASHBYTES(''SHA2_256'', 
                (SELECT ' + @ColumnList + ' 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
            ), 2)) AS segment_hash_id, *
        FROM unfd_positions;
    ';

    -- Step 10: Execute the query to generate the hashid
    EXEC sp_executesql @HashQuery;
END;
GO
