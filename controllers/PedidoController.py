from gestao_pedidos import app
from gestao_pedidos.models.Pedido import Pedido
from flask import request, render_template, redirect, url_for

@app.route('/cadastrar_pedido', methods=['GET', 'POST'])
def cadastrar_pedido():
    if request.method == 'POST':
        data = request.form['data']
        cli_id = request.form['cli_id']
        pedido = Pedido(data, cli_id)
        pedido.save()
        return redirect(url_for('listar_pedidos'))
    return render_template('cadastrar_pedido.html')

@app.route('/listar_pedidos', methods=['GET'])
def listar_pedidos():
    ordem = request.args.get('ordem', 'asc')
    dados = Pedido.get_all(ordem)
    return render_template('listar_pedidos.html', dados=dados, ordem=ordem)
