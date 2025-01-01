DECLARE @JsonString NVARCHAR(MAX);

-- Construct JSON using alias names for hash ID calculation
SELECT @JsonString = STRING_AGG('"' + AliasName + '":"' + ColumnName + '"', ',')
FROM (
    SELECT 
        REPLACE(AliasName, 'Exit_Period', 'business_input') AS AliasName,
        ColumnName
    FROM @Finallist
) AS JsonColumns;

SET @JsonString = '{' + @JsonString + '}';
PRINT @JsonString; -- Debug output
