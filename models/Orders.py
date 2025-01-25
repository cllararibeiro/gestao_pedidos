from gestao_pedidos.database.config import mysql

class Orders:
    def __init__(self, cli_id, data, total):
        self.cli_id = cli_id
        self.data = data
        self.total = total  # Corrigido: total agora é inicializado corretamente.

    def save(self):
        cursor = mysql.connection.cursor()

        # Verificar se o pedido já existe
        cursor.execute(
            "SELECT * FROM tb_pedidos WHERE ped_data = %s AND ped_cli_id = %s",
            (self.data, self.cli_id),
        )
        pedido = cursor.fetchone()

        if pedido:
            cursor.close()
            return {"success": False, "message": "O pedido já está cadastrado!"}

        # Inserir o novo pedido
        cursor.execute(
            "INSERT INTO tb_pedidos (ped_data, ped_cli_id, ped_total) VALUES (%s, %s, %s)",
            (self.data, self.cli_id, self.total),
        )
        mysql.connection.commit()
        cursor.close()

        return {"success": True, "message": "Pedido cadastrado com sucesso!"}

    @staticmethod
    def get_all(ordem='asc'):
        query = f'''
            SELECT 
                ped_id, 
                ped_data, 
                cli_nome, 
                ped_total 
            FROM 
                tb_pedidos 
            JOIN 
                tb_clientes 
            ON 
                ped_cli_id = cli_id 
            ORDER BY 
                ped_data {"ASC" if ordem == "asc" else "DESC"}
        '''
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        dados = cursor.fetchall()
        cursor.close()
        return dados
