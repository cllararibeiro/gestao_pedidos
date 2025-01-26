from gestao_pedidos import app
from gestao_pedidos.database.config import mysql
from flask import render_template, request, flash

@app.route('/relatorios', methods=['GET', 'POST'])
def relatorios():
    resultado = None
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        start_data = request.form.get('start_data', '').strip()
        final_data = request.form.get('final_data', '').strip()
        valor_pedido = request.form.get('valor_pedido', '').strip()
        tops = request.form.get('tops', '').strip()
        intervalo = request.form.get('intervalo', '').strip()

        cursor = mysql.connection.cursor()

        # Base da consulta
        query = """
            SELECT ped_id, cli_nome, ped_total, ped_data 
            FROM tb_pedidos 
            JOIN tb_clientes ON cli_id = ped_cli_id 
            WHERE 1 = 1
        """
        params = []

        # Filtros dinâmicos
        if nome:
            query += " AND cli_nome = %s"
            params.append(nome)

        if start_data and final_data:
            query += " AND ped_data BETWEEN %s AND %s"
            params.append(start_data)
            params.append(final_data)

        if valor_pedido:
            query += " AND ped_total >= %s"
            params.append(valor_pedido)

        if tops and intervalo:
            # Consulta separada para os top produtos
            query = """
                SELECT pro_nome, SUM(proPed_qdproduto) AS qtd_total 
                FROM tb_proPed 
                JOIN tb_produtos ON proPed_pro_id = pro_id 
                WHERE proPed_data BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) AND NOW()
                GROUP BY pro_nome
                ORDER BY qtd_total DESC
                LIMIT %s
            """
            params = [intervalo, tops]

        elif intervalo:
            # Consulta para produtos não vendidos no intervalo
            query = """
                SELECT pro_nome 
                FROM tb_produtos 
                WHERE pro_id NOT IN (
                    SELECT proPed_pro_id 
                    FROM tb_proPed 
                    WHERE proPed_data BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) AND NOW()
                )
            """
            params = [intervalo]

        cursor.execute(query, params)
        resultado = cursor.fetchall()
        cursor.close()

        if not resultado:
            flash("Nenhum dado encontrado para os filtros selecionados.", 'warning')

    return render_template('relatorios.html', resultado=resultado)
