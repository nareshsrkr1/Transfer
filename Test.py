import pyodbc
import json

# Function to fetch active columns (already implemented by you)
def fetch_active_columns():
    # Replace this with your actual implementation to fetch active columns
    return [
        "record_entity_name",
        "maturity_bucket",
        "local_currency",
        "product_liquidity",
        "transaction_type",
        "collateralization",
        "counterparty_type"
    ]

# Database connection setup
def get_db_connection():
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=your_server_name;"
        "DATABASE=your_database_name;"
        "UID=your_username;"
        "PWD=your_password;"
    )
    return conn

# Function to construct and execute the join query
def fetch_data_for_ui():
    # Step 1: Fetch active columns
    active_columns = fetch_active_columns()
    active_columns_str = ", ".join(active_columns)
    
    # Step 2: Construct the query dynamically
    query = f"""
    SELECT 
        -- Default table columns
        {active_columns_str},
        d.exit_strategy AS default_exit_strategy,
        d.exit_phase AS default_exit_phase,
        d.exit_period AS default_exit_period,

        -- Override JSON table columns
        o.exit_strategy_new AS overridden_exit_strategy,
        o.business_input_exit_strategy_new AS business_input_for_exit_strategy,
        o.exit_phase_new AS overridden_exit_phase,
        o.business_input_exit_phase_new AS business_input_for_exit_phase,
        o.exit_period_new AS overridden_exit_period,
        o.business_input_exit_period_new AS business_input_for_exit_period,

        -- Metadata
        o.last_updated_by,
        o.last_updated_on

    FROM 
        default_table AS d
    LEFT JOIN 
        override_json_table AS o
    ON 
        HASHBYTES('SHA2_256', 
            (SELECT {active_columns_str} 
             FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
        ) = o.segment_hash_id;
    """

    # Step 3: Execute the query
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)

    # Step 4: Fetch results and process them for UI
    results = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in results]

    # Close the connection
    conn.close()

    return data

# Main script
if __name__ == "__main__":
    data = fetch_data_for_ui()
    # Print or process the fetched data for UI
    print(json.dumps(data, indent=4))
