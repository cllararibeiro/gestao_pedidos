from gestao_pedidos import app
from gestao_pedidos.controllers import UserController, ClientController, ProductController, OrderController

# @app.route ('/relatorios' , methods=['GET', 'POST'])
# def relatorios():
#     if request.method == 'POST':
#         nome = request.form['nome']
#         start_data = request.form['start_data']
#         final_data = request.form['final_data']
#         valor_pedido = request.form['valor_pedido']
#         tops = request.form['tops']
#         intervalo = request.form['intervalo']
        
#         if nome and start_data and final_data:
#             #total de pedidos em reais por cliente em um intervalo de datas 
#             cursor = mysql.connection.cursor()
#             query = "SELECT ped_total FROM tb_pedidos JOIN tb_clients ON cli_id = ped_cli_id WHERE cli_nome = %s AND ped_data BETWEEN %s AND %s"
#             cursor.execute(query, (nome, start_data, final_data))
#             resultado = cursor.fetchall()
#             cursor.close()

#         elif valor_pedido and start_data and final_data:
#             #clientes com pedidos acima de determinado valor ex: 500 R$
#             cursor = mysql.connection.cursor()
#             query = "SELECT ped_total FROM tb_pedidos JOIN tb_clients ON cli_id = ped_cli_id WHERE ped_total > %s AND ped_data BETWEEN %s AND %s"
#             cursor.execute(query, (valor_pedido, start_data, final_data))
#             resultado = cursor.fetchall()
#             cursor.close()

#         elif tops and intervalo:
#             # top produtos nos intervalos de tempo de 7, 30, 60 e 90 dias 
#             cursor = mysql.connection.cursor()
#             query = """
#                 SELECT proPed_qdproduto, pro_nome FROM tb_proped JOIN tb_produtos ON proPed_pro_id = pro_id 
#                 WHERE proPed_data BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) AND NOW()
#                 ORDER BY proPed_qdproduto DESC
#                 LIMIT %s
#             """
#             cursor.execute(query, (nome, start_data, final_data))
#             resultado = cursor.fetchall()
#             cursor.close()

#         elif intervalo:
#             #produtos não pedidos em intervalos de tempo de 7, 30, 60 e 90 dias 
#             cursor = mysql.connection.cursor()
#             query = """
#                 SELECT pro_nome FROM tb_produtos WHERE pro_id NOT IN (
#                     SELECT proPed_pro_id 
#                     FROM tb_proped 
#                     WHERE proPed_data BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) AND NOW()
#                 )
#             """
#             cursor.execute(query, (nome, start_data, final_data))
#             resultado = cursor.fetchall()
#             cursor.close()
#         else:
#             #caso não seja nenhum desses filtros, ira aparecer esta mensagem de erro
#             flash("Este filtro nâo existe, por favor tentar outro", 'error')

#     return render_template('relatorios.html', resultado = resultado)