def build_dynamic_query_with_mapping(segmentation_columns, override_columns, static_columns, aggregations, column_mapping):
    """
    Builds the dynamic query with proper mapping for UNFD and Override columns.
    
    Args:
        segmentation_columns (list): Active columns for segmentation.
        override_columns (list): Override-specific columns.
        static_columns (list): Static columns to always include.
        aggregations (dict): Aggregations to include in the query.
        column_mapping (dict): Mapping between UNFD and Override columns.
    
    Returns:
        str: The dynamically generated SQL query.
    """
    # Map segmentation columns and static columns
    mapped_segmentation_columns = [
        f"{unfd_col} AS {override_col}" if override_col in column_mapping.values() else unfd_col
        for unfd_col, override_col in column_mapping.items()
        if unfd_col in segmentation_columns
    ]

    # Build the SELECT clause
    select_clause = ",\n    ".join(
        static_columns +
        mapped_segmentation_columns +
        [f"{agg}({col}) AS {alias}" for col, (agg, alias) in aggregations.items()]
    )

    # Build the JOIN condition
    join_conditions = [
        f"up.{unfd_col} = wpd.{override_col}" 
        for unfd_col, override_col in column_mapping.items() 
        if unfd_col in segmentation_columns and override_col in override_columns
    ]
    
    # Assemble the query
    query = f"""
    WITH unifiedPositions AS (
        SELECT
            {select_clause}
        FROM UNFD_POSITIONS_DT
        GROUP BY
            {", ".join(segmentation_columns)}
    )
    SELECT
        {select_clause}
    FROM unifiedPositions up
    LEFT JOIN windDownParams_Override wpd
        ON {' AND '.join(join_conditions)}
    WHERE up.Business_Name = 'CMBS Trading';
    """
    return query
