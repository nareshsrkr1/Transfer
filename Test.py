def extract(expr, visited_ids=None, depth=0):
    try:
        if visited_ids is None:
            visited_ids = set()

        if id(expr) in visited_ids or depth > 50:
            return  # prevent infinite loops or deep nesting

        visited_ids.add(id(expr))

        for select in expr.find_all(Select):
            info["columns"].extend(str(p) for p in select.expressions)

        for table in expr.find_all(Table):
            info["tables"].append(str(table))

        for join in expr.find_all(Join):
            info["joins"].append(str(join))

        for where in expr.find_all(Where):
            info["conditions"].append(str(where.this))

        for group in expr.find_all(Group):
            if group.expressions:
                info["conditions"].extend(str(g) for g in group.expressions)

        for cte in expr.find_all(CTE):
            info["ctes"].append(str(cte))

        if isinstance(expr, Union):
            info["unions"].append(str(expr))

        # NEW: prevent infinite recursion on malformed subqueries
        for subquery in expr.find_all(Subquery):
            extract(subquery, visited_ids, depth + 1)

    except Exception:
        info["unknown"].append(f"Sub-part parse failed:\n{traceback.format_exc()}")
