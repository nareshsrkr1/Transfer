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

    -- Step 5: Add unmapped active columns and create alias expressions for mapped ones
    INSERT INTO @FinalColumns (ColumnExpression)
    SELECT 
        CASE 
            WHEN m.OverrideColumn IS NOT NULL THEN u.ColumnName + ' AS [' + m.OverrideColumn + ']' -- Add alias for mapped columns
            ELSE u.ColumnName -- Unmapped columns remain unchanged
        END
    FROM @ActiveColumns u
    LEFT JOIN @MappedColumns m
        ON u.ColumnName = m.UnfdColumn;

    -- Step 6: Add 'exit_strategy', 'exit_phase', and 'exit_period' if they don’t exist
    IF NOT EXISTS (SELECT 1 FROM @FinalColumns WHERE ColumnExpression LIKE 'exit_strategy%')
        INSERT INTO @FinalColumns (ColumnExpression) VALUES ('exit_strategy');
    IF NOT EXISTS (SELECT 1 FROM @FinalColumns WHERE ColumnExpression LIKE 'exit_phase%')
        INSERT INTO @FinalColumns (ColumnExpression) VALUES ('exit_phase');
    IF NOT EXISTS (SELECT 1 FROM @FinalColumns WHERE ColumnExpression LIKE 'exit_period%')
        INSERT INTO @FinalColumns (ColumnExpression) VALUES ('exit_period');

    -- Step 7: Build the final column list for JSON construction
    SELECT @ColumnList = STRING_AGG(ColumnExpression, ', ')
    FROM @FinalColumns;

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
