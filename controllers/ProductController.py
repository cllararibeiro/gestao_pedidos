from gestao_pedidos import app
from gestao_pedidos.models.Products import Products
from flask import request, redirect, url_for, render_template


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