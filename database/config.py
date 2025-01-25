from gestao_pedidos import app
from flask_mysqldb import MySQL


app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'ayslan_estudo'
app.config['MYSQL_PASSWORD'] = 'estudo'
app.config['MYSQL_DB'] = 'db_pedidos'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def get_connection():       
    conn = mysql.connection()
    return conn