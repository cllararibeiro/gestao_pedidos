from gestao_pedidos import app
from gestao_pedidos.models.Products import Products
from flask import request, redirect, url_for, render_template
from gestao_pedidos.database.config import mysql





@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['precouni']
        quantidade = request.form['quantidade']

        product = Products(nome, descricao, preco, quantidade)
        product.save()

        return redirect(url_for('home'))
    return render_template('cadastrar_produto.html')

@app.route('/listar_produtos', methods=['GET'])
def listar_produtos():
    ordem = request.args.get('ordem', 'asc')
    query = f'SELECT * FROM tb_produtos ORDER BY pro_nome {"ASC" if ordem == "asc" else "DESC"}'
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    dados = cursor.fetchall()
    cursor.close()
    return render_template('listar_produtos.html', dados=dados, ordem=ordem)