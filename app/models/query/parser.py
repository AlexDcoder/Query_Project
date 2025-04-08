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