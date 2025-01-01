-- Step 1: Declare necessary variables
DECLARE @DynamicSQL NVARCHAR(MAX);
DECLARE @JsonColumns NVARCHAR(MAX);
DECLARE @HashIdSql NVARCHAR(MAX);

-- Step 2: Initialize variables
SET @DynamicSQL = 'SELECT ';
SET @JsonColumns = '';
SET @HashIdSql = '';

-- Step 3: Construct the dynamic SQL for columns and JSON generation
SELECT 
    @JsonColumns = @JsonColumns + 
        CASE 
            WHEN fc.AliasName = 'Exit Period' THEN 'exit_period AS business_input, '
            ELSE fc.UfdColumnName + ', '
        END
FROM @FinalColumns fc
ORDER BY fc.SortOrder;

-- Remove the last comma
SET @JsonColumns = LEFT(@JsonColumns, LEN(@JsonColumns) - 2);

-- Step 4: Construct the full dynamic SQL for JSON and Hash ID
SET @DynamicSQL = @DynamicSQL + 
    '(SELECT ' + @JsonColumns + ' FOR JSON PATH, WITHOUT_ARRAY_WRAPPER) AS segment_json, ' +
    'LOWER(CONVERT(VARCHAR(64), HASHBYTES(''SHA2_256'', ' +
    '(SELECT ' + @JsonColumns + ' FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)), 2)) AS segment_hash_id ' +
    'FROM UNFD_POSITIONS_DT';

-- Step 5: Print the dynamic SQL for debugging purposes
PRINT @DynamicSQL;

-- Step 6: Execute the dynamic SQL
EXEC sp_executesql @DynamicSQL;
