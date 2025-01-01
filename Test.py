DECLARE @JsonString NVARCHAR(MAX);

-- Construct JSON string using AliasName and ColumnName
SELECT @JsonString = STRING_AGG('"' + AliasName + '":"' + ColumnName + '"', ',')
FROM FinalColumns;

-- Wrap the result in curly braces to form a valid JSON object
SET @JsonString = '{' + @JsonString + '}';

-- Debug output
PRINT @JsonString;
