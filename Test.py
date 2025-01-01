INSERT INTO @FinalColumns (ColumnExpression, SortOrder)
SELECT 
    -- Add aliases if mapped, otherwise use the column name directly
    CASE 
        WHEN m.OverrideColumn IS NOT NULL THEN u.ColumnName + ' AS [' + m.OverrideColumn + ']'
        ELSE u.ColumnName
    END AS ColumnExpression,
    -- Case-insensitive search for the column in @OrderedColumnList
    CASE 
        WHEN CHARINDEX(',' + LOWER(ISNULL(m.OverrideColumn, u.ColumnName)) + ',', ',' + LOWER(@OrderedColumnList) + ',') > 0 THEN 
            CHARINDEX(',' + LOWER(ISNULL(m.OverrideColumn, u.ColumnName)) + ',', ',' + LOWER(@OrderedColumnList) + ',')
        ELSE 9999 -- Assign a large number for unmatched columns
    END AS SortOrder
FROM @ActiveColumns u
LEFT JOIN @MappedColumns m
    ON LOWER(u.ColumnName) = LOWER(m.UnfdColumn); -- Normalize for case-insensitive join

-- Debug: Output results to verify
SELECT * FROM @FinalColumns;
