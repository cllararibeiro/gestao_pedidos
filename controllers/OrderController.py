from gestao_pedidos import app
from gestao_pedidos.models.Orders import Orders
from gestao_pedidos.database.config import mysql
from gestao_pedidos.models.Client import Client
from flask import request, render_template, redirect, url_for, session,flash

@app.route('/cadastrar_pedido', methods=['GET', 'POST'])
def cadastrar_pedido():
    # Obter clientes e produtos cadastrados
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tb_clientes")
    clientes = cursor.fetchall()

    cursor.execute("SELECT * FROM tb_produtos")
    produtos = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        data = request.form.get('data')
        cli_id = int(request.form.get('cli_id'))
        produtos_selecionados = []
        total_pedido = 0

        # Processar produtos selecionados
        for produto in produtos:
            produto_id = str(produto['pro_id'])
            if produto_id in request.form.getlist('produtos'):
                quantidade = int(request.form.get(f'quantidade_{produto_id}', 1))
                subtotal = produto['pro_preco'] * quantidade
                total_pedido += subtotal
                produtos_selecionados.append({
                    'pro_id': produto['pro_id'],
                    'pro_nome': produto['pro_nome'],
                    'quantidade': quantidade,
                    'subtotal': subtotal
                })

        # Salvar o pedido no banco
        novo_pedido = Orders(cli_id=cli_id, data=data, total=total_pedido, produtos=produtos_selecionados)
        resultado = novo_pedido.save()

        flash(resultado['message'], 'success' if resultado['success'] else 'danger')
        return redirect(url_for('listar_pedidos'))

    return render_template('cadastrar_pedido.html', clientes=clientes, produtos=produtos, produtos_selecionados=[], total_pedido=0)

@app.route('/listar_pedidos', methods=['GET'])
def listar_pedidos():
    ordem = request.args.get('ordem', 'asc')
    dados = Orders.get_all(ordem)
    if dados is None:
        dados = []
    return render_template('listar_pedidos.html', dados=dados, ordem=ordem)
