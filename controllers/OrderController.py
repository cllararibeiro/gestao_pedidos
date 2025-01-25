from gestao_pedidos import app
from gestao_pedidos.models.Orders import Orders
from gestao_pedidos.database.config import mysql
from flask import request, render_template, redirect, url_for, session

@app.route('/cadastrar_pedido', methods=['GET', 'POST'])
@app.route('/cadastrar_pedido', methods=['GET', 'POST'])
def cadastrar_pedido():
    # Garantir que produtos_adicionados esteja na sessão
    if 'produtos_adicionados' not in session or not session['produtos_adicionados']:
        session['produtos_adicionados'] = []

    if request.method == 'POST':
        data = request.form['data']
        cli_id = request.form['cli_id']
        produtos = session['produtos_adicionados']

        # Calcular o total do pedido com base nos preços dos produtos e quantidades
        total_pedido = sum(prod['pro_subtotal'] for prod in produtos)

        # Criar o pedido e salvar no banco
        order = Orders(cli_id, data, total_pedido)
        order.save()

        # Adicionar produtos ao pedido na tabela tb_proPed
        pedido_id = order.get_last_insert_id()  # Assumindo que você tem um método para pegar o ID do último pedido
        for produto in produtos:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO tb_proPed (proPed_ped_id, proPed_pro_id, proPed_qdproduto, proPed_subtotal) VALUES (%s, %s, %s, %s)",
                (pedido_id, produto['pro_id'], produto['pro_qdproduto'], produto['pro_subtotal'])
            )
            mysql.connection.commit()
            cursor.close()

        # Limpar a sessão após o pedido ser salvo
        session['produtos_adicionados'] = []

        return redirect(url_for('listar_pedidos'))

    # Exibir a página de cadastro de pedido
    return render_template('cadastrar_pedido.html')


@app.route('/listar_pedidos', methods=['GET'])
def listar_pedidos():
    ordem = request.args.get('ordem', 'asc')
    dados = Orders.get_all(ordem)
    return render_template('listar_pedidos.html', dados=dados, ordem=ordem)
