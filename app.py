from flask import Flask, jsonify, render_template
import pymysql

app = Flask(__name__)

db_config = {
    'host': 'mysql-2480cbc6-iesb-pi2a2024.h.aivencloud.com',
    'user': 'avnadmin',
    'password': 'AVNS_FhpJunTAM7Hz3pU4pIM',
    'database': 'defaultdb',
    'charset': 'utf8mb4',
    'port': 22150,
    'cursorclass': pymysql.cursors.DictCursor
}

def buscar_dados_tabela():
    connection = pymysql.connect(**db_config)  
    try:
        query = "SELECT * FROM classificacao WHERE colocacao > 0 ORDER BY CAST(colocacao AS UNSIGNED) ASC"
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return jsonify(results)  # Retorna os dados da tabela no formato JSON
    finally:
        connection.close()

@app.route('/')
def index():
    return buscar_dados_tabela()

if __name__ == '__main__':
    app.run(debug=True)
