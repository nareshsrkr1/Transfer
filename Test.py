import json

def format_json_for_hash(ordered_dict):
    """
    Formats the given ordered dictionary into a JSON string:
    - Removes extra spaces.
    - Ensures keys and values use double quotes.
    
    Parameters:
        ordered_dict (dict): The ordered dictionary to format.
    
    Returns:
        str: A JSON string formatted for hash generation.
    """
    return json.dumps(ordered_dict, separators=(',', ':'), ensure_ascii=False)
