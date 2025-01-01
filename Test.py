INSERT INTO @FinalColumns (ColumnExpression, SortOrder)
SELECT 
    CASE 
        WHEN m.OverrideColumn IS NOT NULL THEN u.ColumnName + ' AS [' + m.OverrideColumn + ']'
        ELSE u.ColumnName
    END AS ColumnExpression,
    CHARINDEX(',' + LOWER(ISNULL(m.OverrideColumn, u.ColumnName)) + ',', ',' + LOWER(@OrderedColumnList) + ',') AS SortOrder
FROM @ActiveColumns u
LEFT JOIN @MappedColumns m
    ON LOWER(u.ColumnName) = LOWER(m.UnfdColumn);
