from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

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
        return [vars(atleta) for atleta in colocacao_atletas]

    def buscar_atleta(self, nome):
        for atleta in self.atletas:
            if atleta.nome == nome:
                return atleta
        return None

    def deletar_atleta(self, nome):
        atleta = self.buscar_atleta(nome)
        if atleta:
            self.atletas.remove(atleta)
            return True
        return False

    def atualizar_atleta(self, nome, novo_nome, nova_idade, nova_nacionalidade, nova_colocacao):
        atleta = self.buscar_atleta(nome)
        if atleta:
            atleta.nome = novo_nome
            atleta.idade = nova_idade
            atleta.nacionalidade = nova_nacionalidade
            atleta.colocacao = nova_colocacao
            return True
        return False

    def salvar_atletas(self, connection):
        try:
            with connection.cursor() as cursor:
                for atleta in self.atletas:
                    sql = "INSERT INTO classificacao (nome, idade, nacionalidade, colocacao) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (atleta.nome, atleta.idade, atleta.nacionalidade, atleta.colocacao))
            connection.commit()
            return True
        except pymysql.Error as e:
            print(f"Erro ao salvar dados dos atletas: {e}")
            return False

connection = pymysql.connect(
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    db="defaultdb",
    host="mysql-2480cbc6-iesb-pi2a2024.h.aivencloud.com",
    password="AVNS_FhpJunTAM7Hz3pU4pIM",
    port=22150,
    user="avnadmin",
)

cadastro = CadastroAtletas()

@app.route('/atletas', methods=['GET'])
def listar_atletas():
    atletas = cadastro.listar_atletas()
    return jsonify(atletas), 200

@app.route('/atletas', methods=['POST'])
def adicionar_atleta():
    data = request.json
    atleta = Atleta(data['nome'], data['idade'], data['nacionalidade'], data['colocacao'])
    cadastro.adicionar_atleta(atleta)
    return jsonify({"message": "Atleta adicionado com sucesso!"}), 201

@app.route('/atletas/<nome>', methods=['DELETE'])
def deletar_atleta(nome):
    if cadastro.deletar_atleta(nome):
        return jsonify({"message": "Atleta removido com sucesso!"}), 200
    else:
        return jsonify({"message": "Atleta não encontrado."}), 404

@app.route('/atletas/<nome>', methods=['PUT'])
def atualizar_atleta(nome):
    data = request.json
    if cadastro.atualizar_atleta(nome, data['novo_nome'], data['nova_idade'], data['nova_nacionalidade'], data['nova_colocacao']):
        return jsonify({"message": "Atleta atualizado com sucesso!"}), 200
    else:
        return jsonify({"message": "Atleta não encontrado."}), 404

@app.route('/salvar', methods=['POST'])
def salvar_atletas():
    if cadastro.salvar_atletas(connection):
        return jsonify({"message": "Dados dos atletas salvos no banco de dados."}), 200
    else:
        return jsonify({"message": "Erro ao salvar dados dos atletas."}), 500

if __name__ == '__main__':
    app.run(debug=True)
