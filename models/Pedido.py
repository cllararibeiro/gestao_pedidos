from gestao_pedidos.database.config import mysql
from flask import flash

class Pedido:
    def __init__(self, data, cli_id):
        self.data = data
        self.cli_id = cli_id

    def save(self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tb_pedidos WHERE ped_data = %s AND ped_cli_id = %s", (self.data, self.cli_id))
        pedido = cursor.fetchone()

        if pedido:
            flash("O pedido já está cadastrado!", "danger")
        else:
            cursor.execute(
                "INSERT INTO tb_pedidos (ped_data, ped_cli_id) VALUES (%s, %s)",
                (self.data, self.cli_id)
            )
            mysql.connection.commit()
            flash("Pedido cadastrado com sucesso!", "success")
        cursor.close()
        return True

    @staticmethod
    def get_all(ordem='asc'):
        query = f'SELECT ped_id, ped_data, cli_nome FROM tb_pedidos JOIN tb_clientes ON ped_cli_id = cli_id ORDER BY ped_data {"ASC" if ordem == "asc" else "DESC"}'
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        dados = cursor.fetchall()
        cursor.close()
        return dados
