import pyodbc
from datetime import datetime

def upsert_override_only(data, connection_string):
    """
    Update only override columns or insert a new record into override_json_table.

    Parameters:
        data (dict): The record containing the hash ID and override details.
        connection_string (str): The connection string for the SQL Server database.
    """
    # Extracting relevant fields from the data
    segment_hash_id = data.get('segment_hash_id')
    exit_strategy_override = data.get('exit_strategy_override')
    exit_phase_override = data.get('exit_phase_override')
    business_input_override = data.get('business_input_override')
    last_updated_by = data.get('last_updated_by')
    last_updated_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Establish database connection
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Check if the hash ID exists
    check_query = """
    SELECT COUNT(1)
    FROM override_json_table
    WHERE segment_hash_id = ?
    """
    cursor.execute(check_query, (segment_hash_id,))
    exists = cursor.fetchone()[0] > 0

    if exists:
        # Update override columns if hash ID exists
        update_query = """
        UPDATE override_json_table
        SET 
            exit_strategy_override = ?,
            exit_phase_override = ?,
            business_input_override = ?,
            last_updated_by = ?,
            last_updated_on = ?
        WHERE segment_hash_id = ?
        """
        cursor.execute(update_query, (
            exit_strategy_override,
            exit_phase_override,
            business_input_override,
            last_updated_by,
            last_updated_on,
            segment_hash_id
        ))
    else:
        # Insert a new record with override columns
        insert_query = """
        INSERT INTO override_json_table (
            segment_hash_id,
            exit_strategy_override,
            exit_phase_override,
            business_input_override,
            last_updated_by,
            last_updated_on
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (
            segment_hash_id,
            exit_strategy_override,
            exit_phase_override,
            business_input_override,
            last_updated_by,
            last_updated_on
        ))

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()
