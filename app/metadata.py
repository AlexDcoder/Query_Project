# metadata.py
# Definição dos metadados das tabelas

# Dicionário que representa o esquema do banco de dados fictício.
# Cada chave é o nome de uma tabela, e o valor é uma lista com os nomes das colunas dessa tabela.
TABLES = {
    "Categoria": ["idCategoria", "Descricao"],
    "Produto": ["idProduto", "Nome", "Descricao", "Preco", "QuantEstoque", "Categoria_idCategoria"],
    "TipoCliente": ["idTipoCliente", "Descricao"],
    "Cliente": ["idCliente", "Nome", "Email", "Nascimento", "Senha", "TipoCliente_idTipoCliente", "DataRegistro"],
    "TipoEndereco": ["idTipoEndereco", "Descricao"],
    "Endereco": ["idEndereco", "EnderecoPadrao", "Logradouro", "Numero", "Complemento", "Bairro", "Cidade", "UF", "CEP", "TipoEndereco_idTipoEndereco", "Cliente_idCliente"],
    "Telefone": ["Numero", "Cliente_idCliente"],
    "Status": ["idStatus", "Descricao"],
    "Pedido": ["idPedido", "Status_idStatus", "DataPedido", "ValorTotalPedido", "Cliente_idCliente"],
    "Pedido_has_Produto": ["idPedidoProduto", "Pedido_idPedido", "Produto_idProduto", "Quantidade", "PrecoUnitario"],
    "Tb1": ["nome", "id", "pk", "fk", "sal"],
    "Tb2": ["nome", "id", "pk", "fk", "sal"],
    "Tb3": ["nome", "id", "pk", "fk", "sal"]
}   

# Verifica se uma tabela existe no dicionário de metadados, ignorando diferenças de maiúsculas/minúsculas.
def table_exists(table_name):
    return table_name.lower() in [t.lower() for t in TABLES.keys()]

# Verifica se uma coluna existe dentro de uma tabela específica.
def column_exists(table_name, column_name):
    if not table_exists(table_name):
        return False
    
    # Obtém o nome correto da tabela (com o case original) antes de verificar as colunas
    table_key = next(key for key in TABLES.keys() if key.lower() == table_name.lower())
    return column_name.lower() in [col.lower() for col in TABLES[table_key]]

# Retorna o nome correto da tabela (com o case original), dado um nome qualquer.
def get_correct_table_name(table_name):
    if not table_exists(table_name):
        return None
    return next(key for key in TABLES.keys() if key.lower() == table_name.lower())

# Retorna o nome correto da coluna (com o case original), dado o nome da tabela e da coluna.
def get_correct_column_name(table_name, column_name):
    if not table_exists(table_name) or not column_exists(table_name, column_name):
        return None
    
    table_key = get_correct_table_name(table_name)
    return next(col for col in TABLES[table_key] if col.lower() == column_name.lower())

# Valida colunas qualificadas no formato "tabela.coluna".
# Retorna (True/False, nome_tabela_correto, nome_coluna_correto)
def validate_qualified_column(qualified_column):
    # Divide a string no ponto
    parts = qualified_column.split('.')
    if len(parts) != 2:
        return False, None, None
    
    table_name, column_name = parts[0].strip(), parts[1].strip()
    
    # Verifica se a tabela e a coluna existem
    if not table_exists(table_name):
        return False, None, None
    if not column_exists(table_name, column_name):
        return False, None, None

    # Retorna nomes corrigidos
    correct_table = get_correct_table_name(table_name)
    correct_column = get_correct_column_name(table_name, column_name)
    
    return True, correct_table, correct_column
