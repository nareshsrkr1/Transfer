-- Step 1: Declare variables
DECLARE @HashIdJson NVARCHAR(MAX);
DECLARE @DynamicSQL NVARCHAR(MAX);

-- Initialize the JSON string with the opening brace
SET @HashIdJson = '{';

-- Start constructing the dynamic query
SET @DynamicSQL = '';

-- Dynamically construct the JSON string
SELECT @DynamicSQL = @DynamicSQL + 
    ',"' + fc.AliasName + '": ISNULL(CAST(u.' + fc.ColumnName + ' AS NVARCHAR(MAX)), '''')'
FROM FinalColumns fc
JOIN UNFD u ON fc.ColumnName = u.ColumnName
ORDER BY fc.SortOrder;

-- Remove the leading comma
SET @HashIdJson = @HashIdJson + RIGHT(@DynamicSQL, LEN(@DynamicSQL) - 1);

-- Close the JSON string with the closing brace
SET @HashIdJson = @HashIdJson + '}';

-- Debug: Output the constructed JSON
PRINT 'Constructed JSON: ' + @HashIdJson;

-- Step 2: Generate HashID using the constructed JSON
DECLARE @HashId VARBINARY(64);

-- Generate HashID
SET @HashId = HASHBYTES('SHA2_256', @HashIdJson);

-- Convert to readable hexadecimal format
SELECT LOWER(CONVERT(VARCHAR(64), @HashId, 2)) AS HashId;

-- Debug: Output the HashId
PRINT 'Generated HashId: ' + LOWER(CONVERT(VARCHAR(64), @HashId, 2));
