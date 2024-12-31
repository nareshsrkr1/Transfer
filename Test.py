CREATE PROCEDURE ConstructHashID
AS
BEGIN
    -- Step 1: Get active columns from the config table
    DECLARE @ActiveColumns TABLE (ColumnName NVARCHAR(255));
    INSERT INTO @ActiveColumns (ColumnName)
    SELECT DISTINCT ConfigColumnName
    FROM ConfigTable;

    -- Step 2: Remove 'bidoffspread' column from active columns
    DELETE FROM @ActiveColumns WHERE ColumnName = 'bidoffspread';

    -- Step 3: Map column names from `unfd_or_mapping` table
    DECLARE @MappedColumns TABLE (UnfdColumn NVARCHAR(255), OverrideColumn NVARCHAR(255));
    INSERT INTO @MappedColumns (UnfdColumn, OverrideColumn)
    SELECT UnfdColumn, OverrideColumn
    FROM unfd_or_mapping
    WHERE UnfdColumn IN (SELECT ColumnName FROM @ActiveColumns);

    -- Step 4: Add 'exit_strategy', 'exit_phase', and 'exit_period' if they don’t exist
    IF NOT EXISTS (SELECT 1 FROM @ActiveColumns WHERE ColumnName = 'exit_strategy')
        INSERT INTO @ActiveColumns (ColumnName) VALUES ('exit_strategy');
    IF NOT EXISTS (SELECT 1 FROM @ActiveColumns WHERE ColumnName = 'exit_phase')
        INSERT INTO @ActiveColumns (ColumnName) VALUES ('exit_phase');
    IF NOT EXISTS (SELECT 1 FROM @ActiveColumns WHERE ColumnName = 'exit_period')
        INSERT INTO @ActiveColumns (ColumnName) VALUES ('exit_period');

    -- Step 5: Construct the hashid using the final column list
    DECLARE @ColumnList NVARCHAR(MAX), @HashQuery NVARCHAR(MAX);

    -- Create the JSON format of the columns
    SELECT @ColumnList = STRING_AGG(
        CONCAT('''', m.OverrideColumn, ''', ', m.UnfdColumn), ', ')
    FROM @MappedColumns m;

    SET @HashQuery = '
        SELECT LOWER(CONVERT(VARCHAR(64), 
            HASHBYTES(''SHA2_256'', 
                (SELECT ' + @ColumnList + ' 
                FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
            ), 2)) AS segment_hash_id
        FROM unfd_positions;
    ';

    -- Execute the query to generate the hashid
    EXEC sp_executesql @HashQuery;
END;
