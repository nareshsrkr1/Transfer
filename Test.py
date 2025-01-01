CREATE PROCEDURE ConstructHashID
AS
BEGIN
    -- Step 1: Declare variables and temporary tables
    DECLARE @ActiveColumns TABLE (ColumnName NVARCHAR(255));
    DECLARE @MappedColumns TABLE (UnfdColumn NVARCHAR(255), OverrideColumn NVARCHAR(255));
    DECLARE @FinalColumns TABLE (ColumnName NVARCHAR(255));
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

    -- Step 5: Add 'exit_strategy', 'exit_phase', and 'exit_period' if they don’t exist
    IF NOT EXISTS (SELECT 1 FROM @ActiveColumns WHERE ColumnName = 'exit_strategy')
        INSERT INTO @ActiveColumns (ColumnName) VALUES ('exit_strategy');
    IF NOT EXISTS (SELECT 1 FROM @ActiveColumns WHERE ColumnName = 'exit_phase')
        INSERT INTO @ActiveColumns (ColumnName) VALUES ('exit_phase');
    IF NOT EXISTS (SELECT 1 FROM @ActiveColumns WHERE ColumnName = 'exit_period')
        INSERT INTO @ActiveColumns (ColumnName) VALUES ('exit_period');

    -- Step 6: Build the list of columns for the JSON and hash generation
    INSERT INTO @FinalColumns (ColumnName)
    SELECT OverrideColumn FROM @MappedColumns;

    SELECT @ColumnList = STRING_AGG(ColumnName + ' AS "' + ColumnName + '"', ', ')
    FROM @FinalColumns;

    -- Step 7: Construct the hashid query dynamically
    SET @HashQuery = '
        SELECT LOWER(CONVERT(VARCHAR(64), 
            HASHBYTES(''SHA2_256'', 
                (SELECT ' + @ColumnList + ' 
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
            ), 2)) AS segment_hash_id, *
        FROM unfd_positions;
    ';

    -- Step 8: Execute the query to generate the hashid
    EXEC sp_executesql @HashQuery;
END;
GO
