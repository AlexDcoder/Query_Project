import regex as re
class QueryParser:
    '''
        Componente que analisa e separa os componentes principais da string com a 
        consulta SQL
    '''
    def __init__(self, query_text: str):
        self._quey_text = query_text
        
    def get_selection(self):
        return 'πExpressão(Relação)'
    def get_projection(self):
        return 'σCondição(Relação)'
    def get_junction(self):
        return 'Relação1|x|Relação2'
    
    def parse_sql(sql: str):
        sql = sql.strip().replace('\n', ' ')
        
        select_match = re.search(r'select (.+?) from', sql, re.IGNORECASE)
        from_match = re.search(r'from (.+?)( where |$)', sql, re.IGNORECASE)
        where_match = re.search(r'where (.+)', sql, re.IGNORECASE)

        joins = re.findall(r'join (.+?) on (.+?)(?= join | where |$)', sql, re.IGNORECASE)

        return {
            "select": select_match.group(1).strip().split(',') if select_match else [],
            "from": from_match.group(1).strip() if from_match else '',
            "joins": [{"table": j[0].strip(), "condition": j[1].strip()} for j in joins],
            "where": where_match.group(1).strip() if where_match else ''
        }