import regex as re
from models.db.metadados import METADADOS, OPERATORS

class QueryManager:
    """
    Valida SELECT, FROM, JOIN e WHERE com base nos metadados.
    """
    def __init__(self):
        # Padroniza nomes de tabelas e colunas em UPPER
        self._metadata = {
            tbl.upper(): [col.upper() for col in cols]
            for tbl, cols in METADADOS.items()
        }
        self._logic_ops = {op.upper() for op in OPERATORS}

    def is_valid_table(self, table):
        return table.upper() in self._metadata

    def is_valid_value(self, value, table):
        return value.upper() in self._metadata.get(table.upper(), [])

    def is_select_valid(self, parsed):
        for param in parsed['select']:
            clean = param.strip().strip(',;')
            if '.' not in clean:
                return False
            table, value = clean.split('.', 1)
            if not self.is_valid_table(table) or not self.is_valid_value(value, table):
                return False
        return True

    def is_from_valid(self, parsed):
        return self.is_valid_table(parsed['from'])

    def is_join_valid(self, parsed):
        for join in parsed['joins']:
            if not self.is_valid_table(join['table']):
                return False

            # extrai só table.column
            pairs = re.findall(r'([\w]+)\.([\w]+)', join['condition'])
            for table, value in pairs:
                if not self.is_valid_table(table) or not self.is_valid_value(value, table):
                    return False
        return True

    def is_query_valid(self, parsed):
        return (
            self.is_select_valid(parsed)
            and self.is_from_valid(parsed)
            and self.is_join_valid(parsed)
            # and self.is_where_valid(parsed)  # se implementar
        )