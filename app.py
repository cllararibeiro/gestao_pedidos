from gestao_pedidos import app
from gestao_pedidos.controllers import UserController

#TESTES PARA EDITAR O HTML E CSS
#obs: caso queira colocar em outro lugar, pode colocar 
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/home')
def home():
    return render_template('home.html')
    
@app.route('/cadastrar_clientes')
def cadastrar_clientes():
    return render_template('cadastrar_clientes.html')

@app.route('/cadastrar_pedidos')
def cadastrar_pedidos():
    return render_template('cadastrar_pedidos.html')

@app.route('/cadastrar_produtos')
def cadastrar_produtos():
    return render_template('cadastrar_produtos.html')

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')



