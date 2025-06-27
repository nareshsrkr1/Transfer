import re
import traceback
from sqlglot import parse_one, errors
from sqlglot.expressions import Expression, Select, Table, Join, Subquery, Union

def normalize_query(query: str) -> str:
    # Fix non-standard DATE_SUB(..., 180) to DATE_SUB(..., INTERVAL 180 DAY)
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
            "unions": [],
            "unknown": [f"Parse failed: {e}"]
        }

    info = {
        "columns": [],
        "tables": [],
        "joins": [],
        "conditions": [],
        "unions": [],
        "unknown": []
    }

    def walk(expr):
        try:
            # Handle UNION / UNION ALL
            if isinstance(expr, Union):
                union_type = "UNION" if expr.args.get("distinct") else "UNION ALL"
                info["unions"].append(union_type)
                if expr.args.get("left"):
                    walk(expr.args["left"])
                if expr.args.get("right"):
                    walk(expr.args["right"])
                return

            # Handle SELECT clause
            if isinstance(expr, Select):
                for proj in expr.expressions or []:
                    info["columns"].append(str(proj))

                if expr.args.get("from"):
                    walk(expr.args["from"])

                if expr.args.get("joins"):
                    for join in expr.args["joins"]:
                        walk(join)

                if expr.args.get("where"):
                    condition = expr.args["where"]
                    if condition and condition.this:
                        info["conditions"].append(str(condition.this))

            # Handle tables
            elif isinstance(expr, Table):
                info["tables"].append(str(expr))

            # Handle JOINs
            elif isinstance(expr, Join):
                info["joins"].append(str(expr))
                if expr.args.get("this"):
                    walk(expr.args["this"])
                if expr.args.get("expression"):
                    walk(expr.args["expression"])

            # Handle subqueries
            elif isinstance(expr, Subquery):
                if expr.args.get("this"):
                    walk(expr.args["this"])

            # Recurse on children
            for child in expr.args.values():
                if isinstance(child, Expression):
                    walk(child)
                elif isinstance(child, list):
                    for c in child:
                        if isinstance(c, Expression):
                            walk(c)

        except Exception as e:
            info["unknown"].append(f"Error in walk: {str(e)}\n{traceback.format_exc()}")

    walk(ast)
    return info

# ---------------------
# Sample SQL Query
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

# ---------------------
# Execute and Print Results
# ---------------------
parsed_info = extract_sql_info(query)

for section, items in parsed_info.items():
    print(f"\n=== {section.upper()} ===")
    if not items:
        print("- (none)")
    for item in items:
        print(f"- {item}")
