import re
from sqlglot import parse_one, errors
from sqlglot.expressions import *
import traceback

def normalize_query(query: str) -> str:
    return re.sub(r"date_sub\s*([^,]+),\s*(\d+)", r"date_sub(\1, INTERVAL \2 DAY)", query, flags=re.IGNORECASE)

def extract_sql_info(query: str, dialect="hive"):
    query = normalize_query(query)

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

    def process(expr):
        try:
            if isinstance(expr, Union):
                info["unions"].append("UNION" if expr.args.get("distinct") else "UNION ALL")
                process(expr.args.get("left"))
                process(expr.args.get("right"))

            elif isinstance(expr, Select):
                for col in expr.expressions or []:
                    info["columns"].append(str(col))

                if expr.args.get("from"):
                    for src in expr.args["from"].expressions:
                        process(src)

                if expr.args.get("joins"):
                    for j in expr.args["joins"]:
                        info["joins"].append(str(j))
                        if j.args.get("this"):
                            process(j.args["this"])
                        if j.args.get("expression"):
                            process(j.args["expression"])

                if expr.args.get("where"):
                    info["conditions"].append(str(expr.args["where"].this))

            elif isinstance(expr, Table):
                info["tables"].append(str(expr))

            elif isinstance(expr, Subquery):
                process(expr.args.get("this"))

            # Fallback recursion for any children
            for child in expr.args.values():
                if isinstance(child, Expression):
                    process(child)
                elif isinstance(child, list):
                    for c in child:
                        if isinstance(c, Expression):
                            process(c)

        except Exception:
            info["unknown"].append(traceback.format_exc())

    process(ast)
    return info

# Example Query
query = """
SELECT customer_id,
       CASE WHEN a.use_of_collateral = 'X' THEN 'From' ELSE 'GRB' END AS status_text
FROM accounts a
JOIN customers c ON a.customer_id = c.id
WHERE c.country = 'IN'
UNION ALL
SELECT id, 'Archived' FROM archive_accounts
"""

# Run and print output
parsed = extract_sql_info(query)

for section, values in parsed.items():
    print(f"\n=== {section.upper()} ===")
    if not values:
        print("- (none)")
    else:
        for v in values:
            print(f"- {v}")
