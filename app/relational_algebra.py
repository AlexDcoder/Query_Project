# relational_algebra.py
# Definição de classes para árvore de Álgebra Relacional e conversão de AST (abstract syntax tree)

import re

# Representa uma tabela (relação) no modelo relacional
class Relation:
    def __init__(self, name):
        self.name = name  # Nome da tabela

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

# Representa uma condição booleana (ex: tabela.coluna = valor)
class Condition:
    def __init__(self, expr: str):
        self.expr = expr
        # Extrai todas as colunas qualificadas (ex: tabela.coluna)
        self.columns = re.findall(r'\b\w+\.\w+\b', expr)

    def __str__(self):
        return self.expr

    def __repr__(self):
        return self.__str__()

# Representa um JOIN entre duas relações, com condição
class Join:
    def __init__(self, left, right, condition):
        self.left = left      # Subárvore à esquerda
        self.right = right    # Subárvore à direita
        # A condição pode ser um objeto Condition ou uma string
        self.condition = condition if isinstance(condition, Condition) else Condition(condition)

    def __str__(self):
        return f"({self.left} ⋈_{{{self.condition}}} {self.right})"

    def __repr__(self):
        return self.__str__()

# Representa uma seleção (filtro WHERE)
class Selection:
    def __init__(self, condition, child):
        self.condition = condition if isinstance(condition, Condition) else Condition(condition)
        self.child = child  # Relação ou subárvore a ser filtrada

    def __str__(self):
        return f"σ_{{{self.condition}}}({self.child})"

    def __repr__(self):
        return self.__str__()

# Representa uma projeção (SELECT), ou seja, colunas selecionadas
class Projection:
    def __init__(self, attributes, child):
        self.attributes = attributes  # Lista de atributos: ex. ['clientes.nome', 'pedidos.valor']
        self.child = child           # Subárvore a ser projetada

    def __str__(self):
        cols = ", ".join(self.attributes)
        return f"π_{{{cols}}}({self.child})"

    def __repr__(self):
        return self.__str__()

# Função principal: converte o resultado do parser SQL para uma árvore de álgebra relacional
def ast_to_relational_algebra(parsed_sql: dict):
    """
    Converte o dicionário parsed_sql em uma árvore de Álgebra Relacional.

    parsed_sql deve conter as chaves:
      - 'from': lista de tabelas (strings)
      - 'joins': lista de dicts com 'table' e 'condition'
      - 'where': lista de expressões (strings)
      - 'select': lista de atributos (strings no formato tabela.coluna)
    """
    # 1) Começa com a primeira tabela como raiz
    tables = parsed_sql.get('from', [])
    if not tables:
        raise ValueError("parsed_sql['from'] está vazio")
    root = Relation(tables[0])

    # 2) Aplica os JOINs em sequência (forma associativa à esquerda)
    for join in parsed_sql.get('joins', []):
        right = Relation(join['table'])             # Tabela à direita
        root = Join(root, right, join['condition']) # Novo nó JOIN com raiz atual

    # 3) Aplica as seleções (WHERE) empilhando em cima da árvore
    for cond in parsed_sql.get('where', []):
        root = Selection(cond, root)

    # 4) Aplica a projeção final no topo da árvore
    attrs = parsed_sql.get('select', [])
    root = Projection(attrs, root)

    return root
