import regex as re

def sql_to_algebra(parsed_sql):
    """
    Converte parsed_sql (dicionário com keys 'select', 'from', 'joins', 'where')
    em uma expressão de álgebra relacional usando projeção (π), seleção (σ)
    e theta‑join (⋈_{cond}).
    """
    # 1) Projeção
    proj_cols = ', '.join(parsed_sql['select'])
    projection = f"π[{proj_cols}]"

    # 2) Construção da expressão de join com predicados (theta‑join)
    expr = parsed_sql['from']
    for j in parsed_sql.get('joins', []):
        table = j['table']
        cond  = j['condition']
        # Theta‑join com predicado
        expr = f"{expr} ⨝[{cond}] {table}"

    # 3) Seleção (WHERE) — opcional
    if parsed_sql.get('where'):
        selection = f"σ[{parsed_sql['where']}]"
        expr = f"{selection}({expr})"

    # 4) Aplicar projeção sobre todo o resultado
    return f"{projection}({expr})"

def extract_tables(expression: str):
    return re.findall(r'(\w+)\s*\⨝?', expression)
    
def extract_conditions(expression: str):
    condition_match = re.search(r'σ\[(.*?)\]', expression)
    if condition_match:
        return [cond.strip() for cond in re.split(r'(?i) and ', condition_match.group(1))]
    return []

def extract_projection(expression: str):
    projection_match = re.search(r'π\[(.*?)\]', expression)
    if projection_match:
        return [cond.strip() for cond in re.split(r'(?i) and ', projection_match.group(1))]
    return []

def optimize_algebra(expression: str) -> str:
    projection = extract_projection(expression)
    conditions = extract_conditions(expression)
    tables = extract_tables(expression)

    # Push-down de seleções
    selection_map = {table: [] for table in tables}
    for cond in conditions:
        for table in tables:
            if cond.startswith(table + "."):
                selection_map[table].append(cond)
                break

    # Construção da árvore otimizada em string
    join_expr = " ⨝ ".join([
        f"σ[{ ' and '.join(selection_map[t]) }]({t})" if selection_map[t] else t
        for t in tables
    ])

    if projection:
        return f"π[{', '.join(projection)}]({join_expr})"
    return join_expr