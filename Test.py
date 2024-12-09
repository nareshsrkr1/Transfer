def build_final_query(
    unified_positions_query, 
    segmentation_columns, 
    override_columns, 
    column_mapping, 
    condition_str="up.Business_Name = 'CMBS Trading'"
):
    """
    Constructs the final query with dynamic column selection and join logic.
    
    :param unified_positions_query: The query defining the unifiedPositions CTE.
    :param segmentation_columns: List of columns to be selected from unifiedPositions.
    :param override_columns: List of columns from windDownParams_Override.
    :param column_mapping: Mapping of unifiedPositions to overrides columns.
    :param condition_str: The WHERE condition to be applied dynamically.
    :return: Complete SQL query as a string.
    """
    # Dynamic COALESCE logic for mapped columns
    coalesce_columns = [
        f"COALESCE(wpd.{override_columns[col]}, up.{col}) AS {col}"
        for col in segmentation_columns
        if col in column_mapping.keys() and override_columns.get(column_mapping[col])
    ]

    # Static columns and their respective aliases
    static_selections = [
        "up.Business_Name",
        "up.Records_Entity_Name",
        "up.DerivativeorCash",
        "up.DnT_Product_Type",
        "up.Maturity_Bucket",
        "up.Local_Currency",
        "up.Collateralization",
        "up.Product_Liquidity",
        "up.Trade_count",
        "up.TotalTrade_pct",
        "up.Notional",
        "up.NPV",
        "up.Exit_Strategy_Default",
        "up.Exit_phase_Default",
        "up.Total_Exit_Period_Months",
    ]

    # Selections that require override columns directly
    override_selections = [
        "wpd.Exit_Strategy_BusinessOverride AS Exit_Strategy_Override",
        "wpd.Exit_phase_BusinessOverride AS Exit_phase_Override",
        "wpd.Business_Input AS Business_Input_new",
        "wpd.Business_Input_BusinessOverride AS Business_Input_Override",
        "wpd.RunID",
        "wpd.LastUpdatedBy",
        "wpd.LastUpdatedOn",
        "wpd.HashID",
        "wpd.SegmentationID"
    ]

    # Combine all columns
    final_select_clause = ",\n    ".join(
        static_selections + coalesce_columns + override_selections
    )

    # Dynamic join conditions
    join_conditions = " AND\n    ".join(
        [f"up.{unfd_col} = wpd.{override_col}" for unfd_col, override_col in column_mapping.items()]
    )

    # Final query
    final_query = f"""
    {unified_positions_query}
    SELECT 
        {final_select_clause}
    FROM unifiedPositions up
    LEFT JOIN windDownParams_Override wpd
        ON {join_conditions}
    WHERE {condition_str};
    """
    return final_query


# Example usage
segmentation_columns = [
    "Business_Name",
    "Records_Entity_Name",
    "DnT_Product_Type",
    "DerivativeorCash",
    "Maturity_Bucket",
    "Local_Currency",
    "Collateralization",
    "Product_Liquidity"
]

override_columns = {
    "Business_Name": "Business_Name",
    "Records_Entity_Name": "Records_Entity_Name",
    "DnT_Product_Type": "DnTProduct_Type",
    "DerivativeorCash": "DerivativeorCash",
    "Maturity_Bucket": "Maturity_Bucket",
    "Local_Currency": "Local_Currency",
    "Collateralization": "Collateralization",
    "Product_Liquidity": "Product_Liquidity",
}

column_mapping = {
    "Business_Name": "Business_Name",
    "Records_Entity_Name": "Records_Entity_Name",
    "DnT_Product_Type": "DnTProduct_Type",
    "DerivativeorCash": "DerivativeorCash",
    "Maturity_Bucket": "Maturity_Bucket",
    "Local_Currency": "Local_Currency",
    "Collateralization": "Collateralization",
    "Product_Liquidity": "Product_Liquidity"
}

unified_positions_query = """
WITH unifiedPositions AS (
    SELECT 
        Business_Name,
        Records_Entity_Name,
        DnT_Product_Type,
        DerivativeorCash,
        Maturity_Bucket,
        Local_Currency,
        Collateralization,
        Product_Liquidity,
        SUM(CAST(Current_Position_Netted_MTM_Value_USD AS FLOAT)) AS NPV,
        SUM(ISNULL(CAST(Notional_USD AS FLOAT), 0)) AS Notional,
        COUNT(Transaction_ID_FACS) AS Trade_count,
        'Segment' AS ParamType
    FROM UNFD_POSITIONS_DT
    GROUP BY
        Business_Name,
        Records_Entity_Name,
        DnT_Product_Type,
        DerivativeorCash,
        Maturity_Bucket,
        Local_Currency,
        Collateralization,
        Product_Liquidity
)
"""

# Generate the final query
query = build_final_query(unified_positions_query, segmentation_columns, override_columns, column_mapping)
print(query)
