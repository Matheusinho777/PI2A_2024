from flask import Flask, render_template
import pymysql

app = Flask(__name__)

db_config = {
    'host': 'mysql-2480cbc6-iesb-pi2a2024.h.aivencloud.com',
    'user': 'avnadmin',
    'password': 'AVNS_FhpJunTAM7Hz3pU4pIM',
    'database': 'defaultdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def buscar_dados_tabela():
    connection = pymysql.connect(**db_config)  
    try:
        query = "SELECT * FROM classificacao WHERE colocacao > 0 ORDER BY CAST(colocacao AS UNSIGNED) ASC"
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            print(results)  # Adicionando print para verificar os dados
        return results
    finally:
        connection.close() 

@app.route('/')
def index():
    dados_tabela = buscar_dados_tabela()
    return render_template('index.html', dados_tabela=dados_tabela)

if __name__ == '__main__':
    app.run(debug=True)
