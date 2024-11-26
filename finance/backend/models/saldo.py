from conection import Conexao


class Saldo:
    table: str
    conection: Conexao

    def __init__(self):
        self.table = "saldo"
        self.conection = Conexao

    def create_saldo(self, data: str, saldo: float, fk_banco: int):
        self.conection.execute_query(
            f"INSERT INTO {self.table} (data, saldo, fk_banco) VALUES ({data, saldo, fk_banco})"
        )

    def get_saldo_by_banco(self, fk_banco: int):
        return self.conection.execute_query(
            f"SELECT * FROM {self.table} WHERE fk_banco = {fk_banco}"
        )

    def update_saldo(self, id: int, saldo: float, data: str):
        self.conection.execute_query(
            f"UPDATE {self.table} SET saldo = {saldo} and data = {data} WHERE id = {id}"
        )
