DECLARE @JsonString NVARCHAR(MAX);

-- Construct JSON using alias names for hash ID calculation
SELECT @JsonString = STRING_AGG(
    '"' + 
    REPLACE(AliasName, 'Exit_Period', 'business_input') + '":"'
    + ColumnName + '"', ',')
FROM FinalColumns;

-- Wrap the result in curly braces to form a valid JSON object
SET @JsonString = '{' + @JsonString + '}';

-- Debug output
PRINT @JsonString;
