from gestao_pedidos import app
from gestao_pedidos.controllers import UserController

#TESTES PARA EDITAR O HTML E CSS
#obs: caso queira colocar em outro lugar, pode colocar 
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_pedidos'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tb_clientes WHERE cli_email = %s", (email,))
        cliente = cursor.fetchone()

        if cliente:
            flash("O cliente já está cadastrado!", "danger")
        else:
            cursor.execute(
                "INSERT INTO tb_clientes (cli_nome, cli_email, cli_endereco, cli_telefone) VALUES (%s, %s, %s, %s)",
                (nome, email, endereco, telefone)
            )
            mysql.connection.commit()
            flash("Cadastro efetuado com sucesso!", "success")
        cursor.close()
        return redirect(url_for('index'))
    return render_template('cadastrar_cliente.html')

@app.route ('/relatorios' , methods=['GET', 'POST'])
def relatorios():
    if request.method == 'POST':
        nome = request.form['nome']
        start_data = request.form['start_data']
        final_data = request.form['final_data']
        valor_pedido = request.form['valor_pedido']
        tops = request.form['tops']
        intervalo = request.form['intervalo']
        
        if nome and start_data and final_data:
            #total de pedidos em reais por cliente em um intervalo de datas 
            cursor = mysql.connection.cursor()
            query = "SELECT ped_total FROM tb_pedidos JOIN tb_clients ON cli_id = ped_cli_id WHERE cli_nome = %s AND ped_data BETWEEN %s AND %s"
            cursor.execute(query, (nome, start_data, final_data))
            resultado = cursor.fetchall()
            cursor.close()

        elif valor_pedido and start_data and final_data:
            #clientes com pedidos acima de determinado valor ex: 500 R$
            cursor = mysql.connection.cursor()
            query = "SELECT ped_total FROM tb_pedidos JOIN tb_clients ON cli_id = ped_cli_id WHERE ped_total > %s AND ped_data BETWEEN %s AND %s"
            cursor.execute(query, (valor_pedido, start_data, final_data))
            resultado = cursor.fetchall()
            cursor.close()

        elif tops and intervalo:
            # top produtos nos intervalos de tempo de 7, 30, 60 e 90 dias 
            cursor = mysql.connection.cursor()
            query = """
                SELECT proPed_qdproduto, pro_nome FROM tb_proped JOIN tb_produtos ON proPed_pro_id = pro_id 
                WHERE proPed_data BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) AND NOW()
                ORDER BY proPed_qdproduto DESC
                LIMIT %s
            """
            cursor.execute(query, (nome, start_data, final_data))
            resultado = cursor.fetchall()
            cursor.close()

        elif intervalo:
            #produtos não pedidos em intervalos de tempo de 7, 30, 60 e 90 dias 
            cursor = mysql.connection.cursor()
            query = """
                SELECT pro_nome FROM tb_produtos WHERE pro_id NOT IN (
                    SELECT proPed_pro_id 
                    FROM tb_proped 
                    WHERE proPed_data BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) AND NOW()
                )
            """
            cursor.execute(query, (nome, start_data, final_data))
            resultado = cursor.fetchall()
            cursor.close()

    return render_template('relatorios.html', resultado = resultado)

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['precouni']
        quantidade = request.form['quantidade']

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO tb_produtos (pro_nome, pro_desc, pro_preco, pro_quantidade) VALUES (%s, %s, %s, %s)",
            (nome, descricao, preco, quantidade)
        )
        mysql.connection.commit()
        cursor.close()
        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for('index'))
    return render_template('cadastrar_produto.html')

@app.route('/listar', methods=['GET'])
def listar():
    tipo = request.args.get('tipo', 'pedidos')  # Tipo de listagem: clientes, produtos, pedidos
    ordem = request.args.get('ordem', 'asc')

    # Query de listagem com ordenação
    query = {
        'clientes': f'SELECT * FROM tb_clientes ORDER BY cli_nome {"ASC" if ordem == "asc" else "DESC"}',
        'produtos': f'SELECT * FROM tb_produtos ORDER BY pro_nome {"ASC" if ordem == "asc" else "DESC"}',
        'pedidos': f'SELECT * FROM tb_pedidos ORDER BY ped_data {"ASC" if ordem == "asc" else "DESC"}'
    }.get(tipo, 'SELECT * FROM tb_pedidos ORDER BY ped_data ASC')

    cursor = mysql.connection.cursor()
    cursor.execute(query)
    dados = cursor.fetchall()
    cursor.close()

    return render_template('listar.html', dados=dados, tipo=tipo, ordem=ordem)


@app.route('/home')
def home():
    return render_template('home.html')
