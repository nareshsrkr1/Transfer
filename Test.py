import re
import traceback
from sqlglot import parse_one, errors
from sqlglot.expressions import *

def normalize_query(query: str) -> str:
    # Fix non-standard DATE_SUB(..., 180)
    return re.sub(r"date_sub\s*([^,]+),\s*(\d+)", r"date_sub(\1, INTERVAL \2 DAY)", query, flags=re.IGNORECASE)

def extract_sql_info(raw_query: str, dialect="hive"):
    query = normalize_query(raw_query)

    try:
        ast = parse_one(query, read=dialect)
    except errors.ParseError as e:
        return {
            "columns": [],
            "tables": [],
            "joins": [],
            "conditions": [],
            "ctes": [],
            "unions": [],
            "unknown": [f"Parse failed: {e}"]
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

    def walk(expr):
        try:
            if isinstance(expr, Union):
                # Capture union type
                union_type = "UNION" if expr.args.get("distinct") else "UNION ALL"
                info["unions"].append(union_type)
                walk(expr.args["left"])
                walk(expr.args["right"])

            elif isinstance(expr, Select):
                for proj in expr.expressions:
                    info["columns"].append(str(proj))

                if expr.args.get("where"):
                    info["conditions"].append(str(expr.args["where"].this))

                if expr.args.get("from"):
                    walk(expr.args["from"])

            elif isinstance(expr, Table):
                info["tables"].append(str(expr))

            elif isinstance(expr, Join):
                info["joins"].append(str(expr))
                walk(expr.args.get("this"))
                walk(expr.args.get("expression"))

            elif isinstance(expr, Subquery):
                walk(expr.args.get("this"))

            elif isinstance(expr, CTE):
                info["ctes"].append(str(expr))
                walk(expr.args.get("this"))

            elif isinstance(expr, CTEs):
                for cte in expr.expressions:
                    walk(cte)

            elif isinstance(expr, From):
                for e in expr.expressions:
                    walk(e)

            # Recurse into all child expressions
            for child in expr.args.values():
                if isinstance(child, Expression):
                    walk(child)
                elif isinstance(child, list):
                    for c in child:
                        if isinstance(c, Expression):
                            walk(c)

        except Exception:
            info["unknown"].append(f"Sub-part parse failed:\n{traceback.format_exc()}")

    walk(ast)
    return info

# ---------------------
# Sample Query
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

# Extract and display results
parsed_info = extract_sql_info(query)

for section, items in parsed_info.items():
    print(f"\n=== {section.upper()} ===")
    if not items:
        print("- (none)")
    for i in items:
        print(f"- {i}")
