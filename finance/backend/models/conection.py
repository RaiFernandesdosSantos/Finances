import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError


class Conexao:
    def __init__(self):
        self.host = "localhost"
        self.database = "finance"
        self.user = "postgres"
        self.password = "1234"
        self.port = 5433
        self.cursor_factory = RealDictCursor
        self.conexao = None  # Conexão inicial é None

    def conectar(self):
        if not self.conexao or self.conexao.closed:
            try:
                self.conexao = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                    cursor_factory=self.cursor_factory,
                )
                print("Conexão estabelecida com sucesso!")
            except OperationalError as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
                raise
        return self.conexao

    def desconectar(self):
        try:
            if self.conexao and not self.conexao.closed:
                self.conexao.close()
                print("Conexão fechada com sucesso.")
        except Exception as e:
            print(f"Erro ao fechar a conexão: {e}")
            raise

    def execute_query(self, query, params=None, fetchone=False):
        try:
            with self.conectar().cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone() if fetchone else cursor.fetchall()
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            raise

    def commit(self, query, params=None):
        try:
            with self.conectar().cursor() as cursor:
                cursor.execute(query, params)
                self.conexao.commit()
                print("Alterações aplicadas com sucesso.")
        except Exception as e:
            print(f"Erro ao aplicar alterações: {e}")
            self.conexao.rollback()
            raise
