import re
import csv
import traceback
from sqlglot import parse_one, errors
from sqlglot.expressions import *

def normalize_query(query: str) -> str:
    # Fix non-standard DATE_SUB(..., 180)
    query = re.sub(r"date_sub\s*([^,]+),\s*(\d+)", r"date_sub(\1, INTERVAL \2 DAY)", query, flags=re.IGNORECASE)
    return query

def extract_sql_info(raw_query: str, dialect="hive"):
    query = normalize_query(raw_query)

    try:
        ast = parse_one(query, read=dialect)
    except errors.ParseError:
        return {
            "columns": [],
            "tables": [],
            "joins": [],
            "conditions": [],
            "ctes": [],
            "unions": [],
            "unknown": [f"Failed to parse query: {raw_query}"]
        }

    info = {
        "columns": [],
        "tables": [],
        "joins": [],
        "conditions": [],
        "ctes": [],
        "unions": [],
        "unknown": []
    }

    def extract(expr):
        try:
            if isinstance(expr, Union):
                info["unions"].append(expr.token_type.value)  # UNION or UNION ALL
                # Extract columns inside each part separately
                extract(expr.left)
                extract(expr.right)
                return

            for select in expr.find_all(Select):
                info["columns"].extend(str(p) for p in select.expressions)

            for table in expr.find_all(Table):
                info["tables"].append(str(table))

            for join in expr.find_all(Join):
                info["joins"].append(str(join))

            for where in expr.find_all(Where):
                info["conditions"].append(str(where.this))

            for cte in expr.find_all(CTE):
                info["ctes"].append(str(cte))

            for subquery in expr.find_all(Subquery):
                extract(subquery)

        except Exception:
            info["unknown"].append(f"Sub-part parse failed:\n{traceback.format_exc()}")

    extract(ast)
    return info

def write_csv(info_dict, filename="parsed_sql_output.csv"):
    # Calculate maximum number of rows needed
    max_len = max(len(info_dict["columns"]), 1)

    # Pad all lists to match max_len
    def pad(lst):
        return lst + [''] * (max_len - len(lst))

    data = zip(
        pad(info_dict["columns"]),
        pad(info_dict["tables"]),
        pad(info_dict["joins"]),
        pad(info_dict["conditions"]),
        pad(info_dict["ctes"]),
        pad(info_dict["unions"]),
        pad(info_dict["unknown"]),
    )

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Columns", "Tables", "Joins", "Conditions", "CTEs", "Unions", "Unknown"])
        for row in data:
            writer.writerow(row)

# ---------------------
# Sample Query Input
# ---------------------
query = """
SELECT customer_id,
       CASE WHEN a.use_of_collateral = 'X' THEN 'From' ELSE 'GRB' END AS status_text
FROM accounts a
JOIN customers c ON a.customer_id = c.id
WHERE c.country = 'IN'
UNION ALL
SELECT id, 'Archived' FROM archive_accounts
"""

# Run extractor
info = extract_sql_info(query)

# Save to CSV
write_csv(info)

print("✅ SQL parsed and saved to 'parsed_sql_output.csv'")
