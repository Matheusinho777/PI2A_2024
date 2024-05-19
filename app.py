from flask import Flask, render_template, request, redirect, url_for
from crud.py import Atleta, CadastroAtletas
import pymysql

app = Flask(__name__)

cadastro = CadastroAtletas()

# Conexão com o banco de dados
connection = pymysql.connect(
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    db="defaultdb",
    host="mysql-2480cbc6-iesb-pi2a2024.h.aivencloud.com",
    password="AVNS_FhpJunTAM7Hz3pU4pIM",
    port=22150,
    user="avnadmin",
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = int(request.form['idade'])
        nacionalidade = request.form['nacionalidade']
        colocacao = request.form['colocacao']
        novo_atleta = Atleta(nome, idade, nacionalidade, colocacao)
        cadastro.adicionar_atleta(novo_atleta)
        cadastro.salvar_atletas(connection)
        return redirect(url_for('index'))
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
