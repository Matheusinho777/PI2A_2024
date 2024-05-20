from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def get_db_connection():
    connection = pymysql.connect(
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="mysql-2480cbc6-iesb-pi2a2024.h.aivencloud.com",
        password="AVNS_FhpJunTAM7Hz3pU4pIM",
        port=22150,
        user="avnadmin",
    )
    return connection

@app.route('/atletas', methods=['POST'])
def add_atleta():
    data = request.json
    nome = data['nome']
    idade = data['idade']
    nacionalidade = data['nacionalidade']
    colocacao = data['colocacao']

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        sql = "INSERT INTO classificacao (nome, idade, nacionalidade, colocacao) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome, idade, nacionalidade, colocacao))
        connection.commit()
        return jsonify({'message': 'Atleta adicionado com sucesso!'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'message': 'Erro ao adicionar o atleta', 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
