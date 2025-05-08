# optimizer.py
import re
from copy import deepcopy
from relational_algebra import (
    ast_to_relational_algebra,
    Relation,
    Selection,
    Projection,
    Join,
    Condition
)

# Constrói uma árvore de álgebra relacional (RA) otimizando as seleções
# Aplica seleções de tabela única antes dos JOINs (early selection), 
# depois aplica seleções com múltiplas tabelas e por fim a projeção
def build_ra_with_early_selection(parsed_sql):
    """
    Constrói a árvore de RA aplicando filtros de tabela única antes dos JOINs,
    depois filtros multi-tabela e projeção final.
    """
    # 1) Cria uma relação base para cada tabela no FROM
    base_rel = {tbl.lower(): Relation(tbl) for tbl in parsed_sql.get('from', [])}

    # 2) Aplica seleções que envolvem apenas uma tabela diretamente sobre a relação
    for cond_str in parsed_sql.get('where', []):
        cond = Condition(cond_str)
        tables = {col.split('.')[0].lower() for col in cond.columns}
        if len(tables) == 1:
            tbl = tables.pop()
            if tbl in base_rel:
                base_rel[tbl] = Selection(cond, base_rel[tbl])

    # 3) Executa os JOINs na ordem indicada na cláusula FROM
    root = None
    for tbl in parsed_sql.get('from', []):
        key = tbl.lower()
        if root is None:
            root = base_rel[key]
        else:
            # Busca o JOIN apropriado com base no nome da tabela
            join_info = next(j for j in parsed_sql.get('joins', []) if j['table'].lower() == key)
            join_cond = Condition(join_info['condition'])
            root = Join(root, base_rel[key], join_cond)

    # 4) Aplica seleções que envolvem mais de uma tabela no topo da árvore
    for cond_str in parsed_sql.get('where', []):
        cond = Condition(cond_str)
        tables = {col.split('.')[0].lower() for col in cond.columns}
        if len(tables) > 1:
            root = Selection(cond, root)

    # 5) Aplica projeção final (cláusula SELECT)
    return Projection(parsed_sql.get('select', []), root)


# Empurra a projeção (SELECT) o mais para baixo possível na árvore de RA
# Para evitar trazer colunas desnecessárias
def push_projection_tree(expr):
    """
    Empurra a projeção final para baixo da árvore de joins e seleções.
    """
    if not isinstance(expr, Projection):
        return expr

    proj_attrs = set(expr.attributes)  # Atributos que devem ser mantidos na projeção final

    def push(node, required):
        # Caso base: se for uma relação, aplica projeção diretamente nela
        if isinstance(node, Relation):
            return Projection(list(required), node)

        # Caso de seleção: propaga os atributos necessários para o filho
        if isinstance(node, Selection):
            inner = push(node.child, required)
            return Selection(node.condition, inner)

        # Caso de JOIN: divide os atributos necessários entre os lados do JOIN
        if isinstance(node, Join):
            cond = node.condition
            left_req = set()
            right_req = set()
            for attr in required:
                tbl = attr.split('.')[0].lower()
                if tbl in _rel_names(node.left): left_req.add(attr)
                if tbl in _rel_names(node.right): right_req.add(attr)
            # Adiciona também as colunas usadas na condição de junção
            for col in cond.columns:
                tbl = col.split('.')[0].lower()
                if tbl in _rel_names(node.left): left_req.add(col)
                if tbl in _rel_names(node.right): right_req.add(col)
            left = push(node.left, left_req)
            right = push(node.right, right_req)
            return Join(left, right, cond)

        # Caso padrão: retorna o nó original
        return node

    # Aplica o push a partir do filho da projeção original
    new_root = push(expr.child, proj_attrs)
    return Projection(expr.attributes, new_root)


# Função principal de otimização da consulta
# Aplica as duas estratégias de otimização: seleção antecipada e projeção empurrada
def optimize_query(parsed_sql):
    """
    1) Early selection push-down ao construir RA
    2) Push-down de projeção

    Retorna (árvore_otimizada, passos).
    """
    ra = build_ra_with_early_selection(parsed_sql)  # Otimização com seleção precoce
    steps = ["Early single-table selection push-down"]
    optimized = push_projection_tree(ra)            # Otimização com projeção empurrada
    steps.append("Projection push-down")
    return optimized, steps


# Função auxiliar que retorna os nomes de todas as relações em uma subárvore
def _rel_names(node):
    """Retorna o conjunto de nomes de todas as relações no subtree."""
    if isinstance(node, Relation):
        return {node.name.lower()}
    if hasattr(node, 'child'):
        return _rel_names(node.child)
    if hasattr(node, 'left') and hasattr(node, 'right'):
        return _rel_names(node.left) | _rel_names(node.right)
    return set()
