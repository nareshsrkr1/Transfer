def build_dynamic_query(segmentation_columns, override_columns, static_columns, aggregations):
    """
    Build a dynamic SQL query based on active columns and static logic.
    
    :param segmentation_columns: List of active segmentation columns
    :param override_columns: List of active override columns
    :param static_columns: List of static columns
    :param aggregations: Aggregation mappings for specific columns
    :return: Dynamic SQL query as a string
    """
    # Combine static and dynamic columns
    all_segmentation_columns = list(set(segmentation_columns + static_columns))
    all_override_columns = list(set(override_columns + static_columns))
    
    # Build SELECT and GROUP BY clauses
    select_clause = []
    group_by_clause = []
    for column in all_segmentation_columns:
        if column in aggregations:
            select_clause.append(aggregations[column])
        else:
            select_clause.append(f"up.{column}")
            group_by_clause.append(f"up.{column}")
    
    # Add static calculated fields
    select_clause.extend([
        "'Segment' AS ParamType",
        """
        CAST(
            COUNT(Transaction_ID_FACS) * 100.0 / 
            SUM(COUNT(Transaction_ID_FACS)) OVER (PARTITION BY Business_Name) 
            AS VARCHAR
        ) + '%' AS TotalTrade_pct
        """,
        """
        CASE 
            WHEN Derivative_Transaction_Channel = 'OTC' THEN 
                Derivative_Transaction_Channel + ' ' + ISNULL(Collateralization, '')
            ELSE 
                Derivative_Transaction_Channel 
        END AS Product_Liquidity
        """
    ])
    
    # Dynamically build LEFT JOIN conditions
    join_conditions = []
    for column in all_segmentation_columns:
        join_conditions.append(f"up.{column} = wpd.{column}")
    for column in all_override_columns:
        join_conditions.append(f"up.{column} = wpd.{column}")
    join_condition_string = " AND ".join(join_conditions)
    
    # Build the final SQL query
    query = f"""
    WITH unifiedPositions AS (
        SELECT 
            {", ".join(select_clause)}
        FROM UNFD_POSITIONS_DT
        GROUP BY {", ".join(group_by_clause)}
    )
    SELECT 
        up.*, 
        {", ".join([f"COALESCE(wpd.{col}, up.{col}) AS {col}_Final" for col in all_override_columns])},
        COALESCE(wpd.SegmentationID, 'N/A') AS SegmentationID
    FROM unifiedPositions up
    LEFT JOIN windDownParams_Override wpd
        ON {join_condition_string}
    WHERE up.Business_Name = 'CMBS Trading';
    """
    return query
