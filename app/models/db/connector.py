import mysql.connector
import pandas as pd

class DBConnector:
    def __init__(self, 
        host: str, user: str, password: str, database_name: str) -> None:
        '''
            Inicialização do connector com banco de dados.
        '''
        self.host = host
        self.user = user
        self.password = password
        self.database_name = database_name
        self.db = None
        self.cursor = None

    def start_connection(self) -> None:
        '''
            Iniciar conexão com banco de dados.
        '''
        try:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")
    
    def execute_query(self, query: str) -> pd.DataFrame | None:
        '''
            Executar query no banco de dados
        '''
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            columns = [col[0] for col in self.cursor.description]
            return pd.DataFrame(result, columns=columns)
        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")
    
    def close_connection(self):
        '''
            Fechar conexão com base de dados
        '''
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()