-- Step 1: Declare necessary variables
DECLARE @HashIdJson NVARCHAR(MAX);
DECLARE @HashId VARBINARY(64);

-- Step 2: Assume @FinalColumns table is already populated
-- Example data in @FinalColumns:
-- | ColumnName              | AliasName          | SortOrder |
-- |-------------------------|--------------------|-----------|
-- | Business_Name           | Business Name      | 1         |
-- | Records_Entity_Name     | Records_Entity_Name| 2         |
-- | DnT_Product_Type        | DnTProduct_Type    | 3         |

-- Step 3: Construct JSON dynamically
SELECT @HashIdJson = 
    STRING_AGG('"' + fc.AliasName + '":"' + 
               ISNULL(CAST(u.[ColumnName] AS NVARCHAR(MAX)), '') + '"', ',')
FROM FinalColumns fc
JOIN UNFD u ON fc.ColumnName = u.ColumnName
ORDER BY fc.SortOrder; -- Ensure columns are in the desired order

-- Wrap the JSON string in curly braces
SET @HashIdJson = '{' + @HashIdJson + '}';

-- Debug: Output the constructed JSON
PRINT 'Constructed JSON: ' + @HashIdJson;

-- Step 4: Generate HashID using the constructed JSON
SET @HashId = HASHBYTES('SHA2_256', @HashIdJson);

-- Convert to readable hexadecimal format
SELECT LOWER(CONVERT(VARCHAR(64), @HashId, 2)) AS HashId;

-- Debug: Output the HashId
PRINT 'Generated HashId: ' + LOWER(CONVERT(VARCHAR(64), @HashId, 2));
