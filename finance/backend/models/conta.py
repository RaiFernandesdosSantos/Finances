from conection import Conexao


class Conta:
    def __init__(self):
        self.table = "conta"
        self.conexao = Conexao()

    def create_conta(self, descricao: str):
        try:
            query = f"INSERT INTO {self.table} (descricao) VALUES (%s)"
            self.conexao.commit(query, (descricao,))
        except Exception as e:
            print(f"Erro ao criar conta: {e}")
            raise

    def get_conta_by_name(self, descricao: str):
        try:
            query = f"SELECT * FROM {self.table} WHERE descricao = %s"
            return self.conexao.execute_query(query, (descricao,), fetchone=True)
        except Exception as e:
            print(f"Erro ao buscar conta: {e}")
            raise

    def get_all_contas(self):
        try:
            query = f"SELECT * FROM {self.table}"
            return self.conexao.execute_query(query)
        except Exception as e:
            print(f"Erro ao buscar contas: {e}")
            raise

    def get_conta_by_id(self, id: int):
        try:
            query = f"SELECT * FROM {self.table} WHERE id = %s"
            return self.conexao.execute_query(query, (id,), fetchone=True)
        except Exception as e:
            print(f"Erro ao buscar conta: {e}")
            raise

    def delete_conta(self, id: int):
        try:
            query = f"DELETE FROM {self.table} WHERE id = %s"
            self.conexao.commit(query, (id,))
        except Exception as e:
            print(f"Erro ao deletar conta: {e}")
            raise
