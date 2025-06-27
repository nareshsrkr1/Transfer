import re
from sqlglot import parse_one, errors
from sqlglot.expressions import *
import traceback

def normalize_query(query: str) -> str:
    # Fix non-standard DATE_SUB(..., 180) → DATE_SUB(..., INTERVAL 180 DAY)
    query = re.sub(r"date_sub\s*([^,]+),\s*(\d+)", r"date_sub(\1, INTERVAL \2 DAY)", query, flags=re.IGNORECASE)
    # Add more custom fixes here if needed
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

            if isinstance(expr, Union):
                info["unions"].append(str(expr))

            for subquery in expr.find_all(Subquery):
                extract(subquery)

        except Exception:
            info["unknown"].append(f"Sub-part parse failed:\n{traceback.format_exc()}")

    extract(ast)
    return info

# Example query input
query = """
SELECT customer_id, date_sub(from_unixtime(unix_timestamp()), 180) AS last180days
FROM orders
WHERE status = 'SHIPPED'
UNION ALL
SELECT id, created_at FROM archive_orders
"""

# Run parser
parsed_info = extract_sql_info(query)

# Print structured output
for section, items in parsed_info.items():
    print(f"\n=== {section.upper()} ===")
    for i in items:
        print(f"- {i}")
