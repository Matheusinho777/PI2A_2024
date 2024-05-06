from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'mysql-2480cbc6-iesb-pi2a2024.h.aivencloud.com',
    'user': 'avnadmin',
    'password': 'AVNS_FhpJunTAM7Hz3pU4pIM',
    'database': 'defaultdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Função para buscar os dados da tabela no banco de dados
def buscar_dados_tabela():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Execute a consulta SQL para obter os dados da tabela
            cursor.execute("SELECT * FROM classificacao WHERE colocacao > 0 ORDER BY CAST(colocacao AS UNSIGNED) ASC")
            # Recupere todos os resultados
            results = cursor.fetchall()
            return results
    finally:
        connection.close()

# Rota para renderizar a página
@app.route('/')
def index():
    # Busque os dados da tabela
    dados_tabela = buscar_dados_tabela()
    # Renderize o template e passe os dados da tabela para ele
    return render_template('index.html', dados_tabela=dados_tabela)

if __name__ == '__main__':
    app.run(debug=True)
