from conection import Conexao


class Movimentacao:
    def __init__(self):
        self.table = "movimentacao"
        self.conection = Conexao()

    def get_all_movimentacoes(self):
        try:
            query = f"SELECT * FROM {self.table}"
            return self.conection.execute_query(query)
        except Exception as e:
            print(f"Erro ao buscar movimentações: {e}")
            raise
