from gestao_pedidos import app
from gestao_pedidos.database.config import mysql
from gestao_pedidos.models.Client import Client
from flask import request, render_template, redirect, url_for

@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        client =  Client(nome, email, telefone, endereco)
        client.save()
           
        return redirect(url_for('home'))
    return render_template('cadastrar_cliente.html')

@app.route('/listar_clientes', methods=['GET'])
def listar_clientes():
    ordem = request.args.get('ordem', 'asc')
    query = f'SELECT * FROM tb_clientes ORDER BY cli_nome {"ASC" if ordem == "asc" else "DESC"}'
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    dados = cursor.fetchall()
    cursor.close()
    return render_template('listar_clientes.html', dados=dados, ordem=ordem)




