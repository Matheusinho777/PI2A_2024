from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)  

class Atleta:
    def __init__(self, nome, idade, nacionalidade, colocacao):
        self.nome = nome
        self.idade = idade
        self.nacionalidade = nacionalidade
        self.colocacao = colocacao

class CadastroAtletas:
    def __init__(self):
        self.atletas = []

    def adicionar_atleta(self, atleta):
        self.atletas.append(atleta)

    def listar_atletas(self):
        colocacao_atletas = sorted(self.atletas, key=lambda atleta: atleta.colocacao)
        return [{
            "nome": atleta.nome,
            "idade": atleta.idade,
            "nacionalidade": atleta.nacionalidade,
            "colocacao": atleta.colocacao
        } for atleta in colocacao_atletas]

    def salvar_atletas(self, connection):
        try:
            with connection.cursor() as cursor:
                for atleta in self.atletas:
                    sql = "INSERT INTO classificacao (nome, idade, nacionalidade, colocacao) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (atleta.nome, atleta.idade, atleta.nacionalidade, atleta.colocacao))
            connection.commit()
            print("Dados dos atletas salvos no banco de dados.")
        except pymysql.Error as e:
            print(f"Erro ao salvar dados dos atletas: {e}")

cadastro = CadastroAtletas()


def get_db_connection():
    return pymysql.connect(
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="mysql-2480cbc6-iesb-pi2a2024.h.aivencloud.com",
        password="AVNS_FhpJunTAM7Hz3pU4pIM",
        port=22150,
        user="avnadmin",
    )

@app.route('/atletas', methods=['POST'])
def adicionar_atleta():
    data = request.json
    nome = data.get('nome')
    idade = data.get('idade')
    nacionalidade = data.get('nacionalidade')
    colocacao = data.get('colocacao')
    
    if not all([nome, idade, nacionalidade, colocacao]):
        return jsonify({"message": "Dados incompletos"}), 400

    novo_atleta = Atleta(nome, int(idade), nacionalidade, colocacao)
    cadastro.adicionar_atleta(novo_atleta)

    connection = get_db_connection()
    try:
        cadastro.salvar_atletas(connection)
    finally:
        connection.close()

    return jsonify({"message": "Atleta adicionado com sucesso!"}), 201

@app.route('/atletas', methods=['GET'])
def listar_atletas():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT nome, idade, nacionalidade, colocacao FROM classificacao"
            cursor.execute(sql)
            atletas = cursor.fetchall()
        return jsonify(atletas), 200
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
