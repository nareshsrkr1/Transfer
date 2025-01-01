-- Declare necessary variables for dynamic query construction
DECLARE @HashIdJson NVARCHAR(MAX);
DECLARE @DynamicQuery NVARCHAR(MAX);

-- Step 2: Construct dynamic SQL to build the JSON
SET @DynamicQuery = '
    SELECT @HashIdJson = ''{'' + STRING_AGG(
        ''"'' + fc.AliasName + ''":"'' +
        ' + 'ISNULL(CAST(u.' + QUOTENAME('fc.ColumnName') + ' AS NVARCHAR(MAX)), '''') + ''''',' +
        ''''') + ''}'' ' +
    'FROM @FinalColumns fc ' +
    'JOIN UNFD u ON fc.ColumnName = u.ColumnName ' + 
    'ORDER BY fc.SortOrder'; -- Ensures the columns are ordered based on the SortOrder

-- Debug: Print dynamic query for review
PRINT @DynamicQuery;

-- Step 3: Execute the dynamic query to construct the JSON string
EXEC sp_executesql @DynamicQuery, N'@HashIdJson NVARCHAR(MAX) OUTPUT', @HashIdJson OUTPUT;

-- Step 4: Debug the constructed JSON
PRINT 'Constructed JSON: ' + @HashIdJson;
