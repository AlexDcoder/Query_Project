def sql_to_algebra(parsed_sql):
    proj = f"π[{', '.join(parsed_sql['select'])}]"
    joins = [parsed_sql["from"]] + [j["table"] for j in parsed_sql["joins"]]
    join_expr = ' ⨝ '.join(joins)

    if parsed_sql["where"]:
        sel = f"σ[{parsed_sql['where']}]"
        return f"{proj}({sel}({join_expr}))"
    else:
        return f"{proj}({join_expr})"