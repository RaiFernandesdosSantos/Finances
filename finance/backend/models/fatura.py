from conection import Conexao


class Fatura:
    table: str
    conexao: Conexao

    def __init__(self):
        self.table = "fatura"
        self.conexao = Conexao

    def create_fatura(
        self, fk_cartao: int, fechamento: str, vencimento: str, estado: str
    ):
        query = f"INSERT INTO {self.table} (fk_cartao, fechamento, vencimento, estado) VALUES (%s, %s, %s, %s)"
        self.conexao.commit(query, (fk_cartao, fechamento, vencimento, estado))

    def get_all_faturas(self):
        query = f"SELECT * FROM {self.table}"
        return self.conexao.execute_query(query)

    def get_fatura_by_id(self, id: int):
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        return self.conexao.execute_query(query, (id,), fetchone=True)

    def get_fatura_by_fk_cartao(self, fk_cartao: int):
        query = f"SELECT * FROM {self.table} WHERE fk_cartao = %s"
        return self.conexao.execute_query(query, (fk_cartao,), fetchone=True)

    def get_fatura_by_vencimento(self, vencimento: str):
        query = f"SELECT * FROM {self.table} WHERE vencimento = %s"
        return self.conexao.execute_query(query, (vencimento,), fetchone=True)

    def update_fatura(self, id: int, fechamento: str, vencimento: str, estado: str):
        query = f"UPDATE {self.table} SET fechamento = %s, vencimento = %s, estado = %s WHERE id = %s"
        self.conexao.commit(query, (fechamento, vencimento, estado, id))

    def delete_fatura(self, id: int):
        query = f"DELETE FROM {self.table} WHERE id = %s"
        self.conexao.commit(query, (id,))
