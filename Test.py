def build_dynamic_join_conditions(mapped_segmentation_columns):
    """
    Build dynamic join conditions based on mapped columns.
    """
    join_conditions = [
        f"up.{unfd_col} = wpd.{override_col}"
        for unfd_col, override_col in mapped_segmentation_columns
    ]
    return " AND\n    ".join(join_conditions)

def build_dynamic_query(
    static_columns,
    mapped_segmentation_columns,
    aggregations,
):
    """
    Build a dynamic SQL query with explicit joins and column mappings.
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

    # Build the JOIN clause dynamically
    join_clause = build_dynamic_join_conditions(mapped_segmentation_columns)

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


from sqlalchemy import create_engine
from constants import STATIC_COLUMNS, AGGREGATIONS
import pandas as pd

# Create a database connection
engine = create_engine("your_database_connection_string")

# Fetch active columns
segmentation_columns = get_active_columns(engine, "config_dynamic_segmentation")

# Fetch column mappings filtered by selected columns
mapped_segmentation_columns = get_column_mapping(engine, segmentation_columns)

# Build the dynamic query
query = build_dynamic_query(
    static_columns=STATIC_COLUMNS,
    mapped_segmentation_columns=mapped_segmentation_columns,
    aggregations=AGGREGATIONS,
)

# Print the final query
print(query)
