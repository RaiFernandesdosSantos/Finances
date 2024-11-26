from saldo import Saldo
from conta import Conta


class Banco(Conta):
    table: str
    saldo: Saldo

    def __init__(self):
        self.table = "banco"
        self.saldo = Saldo()
        super().__init__()

    def create_banco(
        self,
        descricao: str,
        agencia: str,
        tipo_instituicao: str,
        conta: str,
        data: str,
        saldo: float,
    ):
        query_banco = f"INSERT INTO {self.table} (descricao, agencia, tipo_instituicao, conta) VALUES (%s, %s, %s, %s)"
        self.conexao.commit(query_banco, (descricao, agencia, tipo_instituicao, conta))

        banco = self.get_conta_by_name(descricao)

        query_saldo = f"INSERT INTO {self.saldo.table} (data, saldo, fk_banco) VALUES (%s, %s, %s)"
        self.saldo.create_saldo(data, saldo, banco["id"])

    def get_all_bancos(self):
        return self.conexao.execute_query(f"SELECT * FROM {self.table}")

    def get_banco_by_id(self, id: int):
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        return self.conexao.execute_query(query, (id,), fetchone=True)

    def update_banco(
        self, id: int, descricao: str, agencia: str, tipo_instituicao: str, conta: str
    ):
        query = f"UPDATE {self.table} SET descricao = %s, agencia = %s, tipo_instituicao = %s, conta = %s WHERE id = %s"
        self.conexao.commit(query, (descricao, agencia, tipo_instituicao, conta, id))
