import pyodbc
import hashlib
import json
from datetime import datetime

# Database connection details
connection = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=your_server;"
    "Database=your_database;"
    "Trusted_Connection=yes;"
)

# Function to upsert the override_table
def upsert_override_table(segment_data, overrides, last_updated_by):
    """
    Insert or update the override_table with segment JSON and override details.
    
    Args:
    - segment_data (dict): Active segments as key-value pairs.
    - overrides (dict): New override values for exit_strategy, exit_phase, and exit_period.
    - last_updated_by (str): The user performing the update.
    """
    try:
        cursor = connection.cursor()

        # Generate JSON and hash
        segment_json = json.dumps(segment_data, sort_keys=True)  # Ensure consistent order for hashing
        segment_hash = hashlib.sha256(segment_json.encode()).hexdigest()

        # Check if the hash exists in the table
        check_query = "SELECT id FROM override_table WHERE segment_hash_id = ?"
        cursor.execute(check_query, segment_hash)
        existing = cursor.fetchone()

        if existing:
            # Update the existing record
            update_query = """
            UPDATE override_table
            SET 
                exit_strategy_new = ?,
                exit_phase_new = ?,
                exit_period_new = ?,
                last_updated_by = ?,
                last_updated_on = ?
            WHERE segment_hash_id = ?
            """
            cursor.execute(
                update_query,
                overrides.get("exit_strategy"),
                overrides.get("exit_phase"),
                overrides.get("exit_period"),
                last_updated_by,
                datetime.now(),
                segment_hash
            )
            print(f"Updated record with hash {segment_hash}")
        else:
            # Insert a new record
            insert_query = """
            INSERT INTO override_table (segment_json, segment_hash_id, exit_strategy_new, exit_phase_new, exit_period_new, last_updated_by, last_updated_on)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(
                insert_query,
                segment_json,
                segment_hash,
                overrides.get("exit_strategy"),
                overrides.get("exit_phase"),
                overrides.get("exit_period"),
                last_updated_by,
                datetime.now()
            )
            print(f"Inserted new record with hash {segment_hash}")

        # Commit the transaction
        connection.commit()

    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()

# Example Usage
if __name__ == "__main__":
    # Active segments fetched dynamically
    active_segments = {
        "active_segment_1": "Segment1_Value",
        "active_segment_2": "Segment2_Value",
        "active_segment_3": "Segment3_Value"
    }

    # Overrides from user input or UI
    overrides = {
        "exit_strategy": "Residual",
        "exit_phase": "Phase 2",
        "exit_period": 12
    }

    # Last updated by
    last_updated_by = "User1"

    # Perform upsert
    upsert_override_table(active_segments, overrides, last_updated_by)
