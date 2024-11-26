from conection import Conexao


class Categoria:
    table: str
    conexao: Conexao

    def __init__(self):
        self.table = "categoria"
        self.conexao = Conexao()

    def create_categoria(self, descricao: str, tipo_categoria: str):
        try:
            if tipo_categoria not in ["R", "D"]:
                raise ValueError(
                    "O tipo de categoria deve ser 'R' para receita ou 'D' para despesa."
                )
            query = (
                f"INSERT INTO {self.table} (descricao, tipo_categoria) VALUES (%s, %s)"
            )
            self.conexao.commit(query, (descricao, tipo_categoria))
        except Exception as e:
            print(f"Erro ao criar categoria: {e}")
            raise

    def get_all_categorias(self):
        try:
            query = f"SELECT * FROM {self.table}"
            return self.conexao.execute_query(query)
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            raise

    def get_all_categoria_by_tipo(self, tipo: str):
        try:
            if tipo not in ["R", "D"]:
                raise ValueError(
                    "O tipo de categoria deve ser 'R' para receita ou 'D' para despesa."
                )
            query = f"SELECT * FROM {self.table} WHERE tipo_categoria = %s"
            return self.conexao.execute_query(query, (tipo,))
        except Exception as e:
            print(f"Erro ao buscar categorias: {e}")
            raise

    def get_categoria_by_id(self, id: int):
        try:
            query = f"SELECT * FROM {self.table} WHERE id = %s"
            return self.conexao.execute_query(query, (id,), fetchone=True)
        except Exception as e:
            print(f"Erro ao buscar categoria: {e}")
            raise

    def update_categoria(self, id: int, descricao: str, tipo_categoria: str):
        try:
            if tipo_categoria not in ["R", "D"]:
                raise ValueError(
                    "O tipo de categoria deve ser 'R' para receita ou 'D' para despesa."
                )

            query = f"UPDATE {self.table} SET descricao = %s, tipo_categoria = %s WHERE id = %s"
            self.conexao.commit(query, (descricao, tipo_categoria, id))
        except Exception as e:
            print(f"Erro ao atualizar categoria: {e}")
            raise

    def delete_categoria(self, id: int):
        try:
            query = f"DELETE FROM {self.table} WHERE id = %s"
            self.conexao.commit(query, (id,))
        except Exception as e:
            print(f"Erro ao deletar categoria: {e}")
            raise
