-- Step 1: Declare necessary variables
DECLARE @HashIdJson NVARCHAR(MAX);
DECLARE @DynamicSQL NVARCHAR(MAX);

-- Initialize the JSON string with the opening brace
SET @HashIdJson = '{';

-- Step 2: Build the dynamic SQL query to generate the JSON string
SET @DynamicSQL = '';

-- Dynamically construct the JSON string
SELECT @DynamicSQL = @DynamicSQL + 
    ',"' + fc.AliasName + '": ISNULL(CAST(u.' + fc.ColumnName + ' AS NVARCHAR(MAX)), '''')'
FROM FinalColumns fc
JOIN UNFD u ON fc.ColumnName = u.ColumnName -- Map to the actual columns in UNFD
ORDER BY fc.SortOrder;  -- Ensure the columns are in the correct order

-- Remove the leading comma
SET @HashIdJson = @HashIdJson + RIGHT(@DynamicSQL, LEN(@DynamicSQL) - 1);

-- Close the JSON string with the closing brace
SET @HashIdJson = @HashIdJson + '}';

-- Debug: Output the constructed JSON
PRINT 'Constructed JSON: ' + @HashIdJson;

-- Step 3: Generate HashID using the constructed JSON
DECLARE @HashId VARBINARY(64);

-- Generate the HashID
SET @HashId = HASHBYTES('SHA2_256', @HashIdJson);

-- Convert to readable hexadecimal format
SELECT LOWER(CONVERT(VARCHAR(64), @HashId, 2)) AS HashId;

-- Debug: Output the HashId
PRINT 'Generated HashId: ' + LOWER(CONVERT(VARCHAR(64), @HashId, 2));
