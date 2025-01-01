-- Declare necessary variables
DECLARE @HashIdJson NVARCHAR(MAX);

-- Initialize the JSON string with an opening brace
SET @HashIdJson = '{';

-- Construct the JSON string manually, adding each field dynamically based on @FinalColumns
-- Note: Make sure to adapt this to match the number of records in your FinalColumns table

SELECT @HashIdJson = @HashIdJson + 
    '"' + fc.AliasName + '":' + 
    'ISNULL(CAST(u.' + fc.ColumnName + ' AS NVARCHAR(MAX)), '''')' + 
    ','  -- Add a comma for each entry except the last one
FROM FinalColumns fc
JOIN UNFD u ON fc.ColumnName = u.ColumnName
ORDER BY fc.SortOrder;

-- Remove the last comma (if any) and close the JSON string with a closing brace
SET @HashIdJson = LEFT(@HashIdJson, LEN(@HashIdJson) - 1) + '}';

-- Debug: Output the constructed JSON
PRINT 'Constructed JSON: ' + @HashIdJson;
