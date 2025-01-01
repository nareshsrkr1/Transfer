-- Step 1: Declare necessary variables
DECLARE @JsonString NVARCHAR(MAX);
DECLARE @DynamicSQL NVARCHAR(MAX);
DECLARE @HashId VARBINARY(64);

-- Step 2: Initialize the JSON string
SET @JsonString = '{';

-- Step 3: Build the dynamic SQL query to generate the JSON string
SET @DynamicSQL = '';

-- Dynamically construct the JSON string based on AliasName and the corresponding values from UNFD
SELECT @DynamicSQL = @DynamicSQL + 
    ', "' + LOWER(fc.AliasName) + '": ISNULL(CAST(u.' + fc.UfdColumnName + ' AS NVARCHAR(MAX)), '''')'
FROM @FinalColumns fc
JOIN unfd_positions_dt u ON fc.UfdColumnName = u.ColumnName  -- This will join the correct column name
ORDER BY fc.SortOrder;  -- Ensure the columns are in the correct order

-- Remove the leading comma from @DynamicSQL
SET @JsonString = @JsonString + RIGHT(@DynamicSQL, LEN(@DynamicSQL) - 1);

-- Close the JSON string with the closing brace
SET @JsonString = @JsonString + '}';

-- Debug: Output the constructed JSON
PRINT 'Constructed JSON: ' + @JsonString;

-- Step 4: Generate HashID using the constructed JSON
SET @HashId = HASHBYTES('SHA2_256', @JsonString);

-- Convert to readable hexadecimal format
SELECT LOWER(CONVERT(VARCHAR(64), @HashId, 2)) AS HashId;

-- Debug: Output the HashId
PRINT 'Generated HashId: ' + LOWER(CONVERT(VARCHAR(64), @HashId, 2));
