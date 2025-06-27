import sqlglot
from sqlglot import parse_one

sql = """
SELECT c.customer_id as cust_id, o.order_id, o.order_date, p.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN payments p ON o.order_id = p.order_id
WHERE o.status = 'ACTIVE' AND p.payment_date > '2024-01-01'
"""

# Parse the SQL
tree = parse_one(sql)

# Extract columns
columns = [str(e) for e in tree.expressions]

# Extract table names
tables = [str(t) for t in tree.find_all(sqlglot.expressions.Table)]

# Extract joins and where
joins = [str(j) for j in tree.find_all(sqlglot.expressions.Join)]
where_clause = str(tree.args.get("where")) if tree.args.get("where") else ""

# Now structure the output
import pandas as pd

df = pd.DataFrame(columns=["Columns Selected", "Tables Involved", "Joins & Conditions"])

# Add a row per column
for col in columns:
    df.loc[len(df)] = [col, ", ".join(tables), "; ".join(joins) + "; " + where_clause]

print(df)
