def build_dynamic_query_with_explicit_aliases(
    static_columns,
    mapped_segmentation_columns,
    aggregations,
    join_conditions,
):
    """
    Build a dynamic SQL query, ensuring all columns are prefixed with explicit table aliases.

    Args:
        static_columns: List of static column names (from `UNFD`).
        mapped_segmentation_columns: List of (unfd_column, override_column) tuples.
        aggregations: Dictionary of aggregation columns and their SQL logic.
        join_conditions: List of join conditions between UNFD and Override tables.

    Returns:
        A dynamically generated SQL query as a string.
    """
    # Prefix static columns with "up."
    prefixed_static_columns = [f"up.{col}" for col in static_columns]

    # Prefix mapped segmentation columns with explicit aliases
    prefixed_mapped_columns = [
        f"up.{unfd_col} AS {override_col}" for unfd_col, override_col in mapped_segmentation_columns
    ]

    # Build the SELECT clause
    select_clause = ",\n    ".join(
        prefixed_static_columns + prefixed_mapped_columns + list(aggregations.values())
    )

    # Build the JOIN clause
    join_clause = " AND\n    ".join(
        [f"up.{unfd_col} = wpd.{override_col}" for unfd_col, override_col in join_conditions]
    )

    query = f"""
    WITH unifiedPositions AS (
        SELECT 
            {",\n            ".join(prefixed_static_columns)},
            {",\n            ".join(aggregations.values())}
        FROM UNFD_POSITIONS_DT up
        GROUP BY 
            {", ".join(prefixed_static_columns)}
    )
    SELECT 
        {select_clause}
    FROM unifiedPositions up
    LEFT JOIN windDownParams_Override wpd
        ON {join_clause}
    WHERE up.Business_Name = 'CMBS Trading';
    """
    return query
