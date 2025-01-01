DECLARE @JsonString NVARCHAR(MAX);

-- Construct JSON using alias names for hash ID calculation
SELECT @JsonString = STRING_AGG(
    '"' + 
    CASE 
        WHEN CHARINDEX(' AS ', ColumnExpression) > 0 
        THEN RIGHT(ColumnExpression, LEN(ColumnExpression) - CHARINDEX(' AS ', ColumnExpression) - 3)
        ELSE ColumnExpression
    END 
    + '":"'
    +
    CASE 
        WHEN CHARINDEX(' AS ', ColumnExpression) > 0 
        THEN LEFT(ColumnExpression, CHARINDEX(' AS ', ColumnExpression) - 1)
        ELSE ColumnExpression
    END 
    + '"', ',')
FROM (
    SELECT 
        REPLACE(
            CASE 
                WHEN CHARINDEX(' AS ', ColumnExpression) > 0 
                THEN RIGHT(ColumnExpression, LEN(ColumnExpression) - CHARINDEX(' AS ', ColumnExpression) - 3)
                ELSE ColumnExpression
            END, 
            'Exit_Period', 
            'business_input'
        ) AS AliasName,
        CASE 
            WHEN CHARINDEX(' AS ', ColumnExpression) > 0 
            THEN LEFT(ColumnExpression, CHARINDEX(' AS ', ColumnExpression) - 1)
            ELSE ColumnExpression
        END AS ColumnName
    FROM @Finallist
) AS JsonColumns;

SET @JsonString = '{' + @JsonString + '}';
PRINT @JsonString; -- Debug output
