-- Step 1: Declare necessary variables
DECLARE @HashIdJson NVARCHAR(MAX);
DECLARE @HashId VARBINARY(64);
DECLARE @DynamicQuery NVARCHAR(MAX);
DECLARE @FinalColumns TABLE (
    ColumnName NVARCHAR(128),
    AliasName NVARCHAR(128),
    SortOrder INT
);

-- Example data in @FinalColumns
INSERT INTO @FinalColumns (ColumnName, AliasName, SortOrder)
VALUES
    ('Business_Name', 'Business Name', 1),
    ('Records_Entity_Name', 'Records_Entity_Name', 2),
    ('DnT_Product_Type', 'DnTProduct_Type', 3),
    ('DerivativeorCash', 'DerivativeorCash', 4),
    ('Maturity_Bucket', 'Maturity_Bucket', 5),
    ('Currency_DT', 'Local_Currency', 6),
    ('Derivative_Transaction_Channel', 'Transaction_Type', 7),
    ('Collateralization', 'Collateralization', 8),
    ('Counterparty_Type', 'CounterParty_Type', 9),
    ('Product_Liquidity', 'Product_Liquidity', 10),
    ('Banking TradingFlag', 'BankingTradingFlag', 11),
    ('Exit_Strategy', 'Exit_Strategy', 12),
    ('Exit_Phase', 'Exit_Phase', 13);

-- Step 2: Construct JSON dynamically using the ColumnName and AliasName
SET @DynamicQuery = 
    'SELECT @HashIdJson = ''{'' + STRING_AGG(' +
    ' ''"'' + fc.AliasName + ''":"' +
    ' ISNULL(CAST(u.[' + fc.ColumnName + '] AS NVARCHAR(MAX)), '''') + ''"'',' +
    ' '') + ''}'' ' +
    'FROM @FinalColumns fc ' +
    'JOIN UNFD u ON fc.ColumnName = u.ColumnName ' + -- Ensure we match column names correctly
    'ORDER BY fc.SortOrder';

-- Debug: Print dynamic query for review
PRINT @DynamicQuery;

-- Step 3: Execute the dynamic query
EXEC sp_executesql @DynamicQuery, N'@HashIdJson NVARCHAR(MAX) OUTPUT', @HashIdJson OUTPUT;

-- Step 4: Debug the constructed JSON
PRINT 'Constructed JSON: ' + @HashIdJson;

-- Step 5: Generate HashID using the constructed JSON
SET @HashId = HASHBYTES('SHA2_256', @HashIdJson);

-- Convert to readable hexadecimal format
SELECT LOWER(CONVERT(VARCHAR(64), @HashId, 2)) AS HashId;

-- Debug: Output the HashId
PRINT 'Generated HashId: ' + LOWER(CONVERT(VARCHAR(64), @HashId, 2));
