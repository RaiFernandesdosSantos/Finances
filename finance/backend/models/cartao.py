from conta import Conta


class Cartao(Conta):
    table: str

    def __init__(self):
        self.table = "cartao"
        super().__init__()

    def create_cartao(
        self,
        descricao: str,
        limite: float,
        dia_vencimento: int,
        fk_banco: int,
        bandeira: str,
    ):
        try:
            if limite < 0:
                raise ValueError("O limite não pode ser negativo")
            if not 1 <= dia_vencimento <= 31:
                raise ValueError("Dia vencimento inválido")

            query = f"INSERT INTO {self.table} (descricao, limite, dia_vencimento, fk_banco, bandeira) VALUES (%s, %s, %s, %s, %s)"
            self.conexao.commit(
                query, (descricao, limite, dia_vencimento, fk_banco, bandeira)
            )
        except Exception as e:
            print(f"Erro ao criar cartão: {e}")
            raise

    def get_cartao_by_id(self, id: int):
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        return self.conexao.execute_query(query, (id,), fetchone=True)

    def get_all_cartoes(self):
        query = f"SELECT * FROM {self.table}"
        return self.conexao.execute_query(query)

    def update_cartao(
        self,
        id: int,
        descricao: str,
        limite: float,
        dia_vencimento: int,
        fk_banco: int,
        bandeira: str,
    ):
        try:
            if limite < 0:
                raise ValueError("O limite não pode ser negativo")
            if not 1 <= dia_vencimento <= 31:
                raise ValueError("Dia vencimento invático")

            query = f"UPDATE {self.table} SET descricao = %s, limite = %s, dia_vencimento = %s, fk_banco = %s, bandeira = %s WHERE id = %s"
            self.conexao.commit(
                query, (descricao, limite, dia_vencimento, fk_banco, bandeira, id)
            )
        except Exception as e:
            print(f"Erro ao atualizar cartão: {e}")
            raise
