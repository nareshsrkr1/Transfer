import re
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
            # Handle UNION and distinguish UNION vs UNION ALL
            if isinstance(expr, Union):
                union_type = "UNION" if expr.args.get("distinct") else "UNION ALL"
                info["unions"].append(union_type)
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

# ---------------------
# Test Query
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

# Parse and print results
parsed_info = extract_sql_info(query)

for section, items in parsed_info.items():
    print(f"\n=== {section.upper()} ===")
    if not items:
        print("- (none)")
    for i in items:
        print(f"- {i}")
