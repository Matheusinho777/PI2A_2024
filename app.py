from flask import Flask, render_template
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pymysql
import pandas as pd

app = Flask(__name__)

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
    query = "SELECT * FROM classificacao WHERE colocacao > 0 ORDER BY CAST(colocacao AS UNSIGNED) ASC"
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    df = pd.DataFrame(results)

    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}]]
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=df.columns,
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[df[k].tolist() for k in df.columns],
                align="left")
        ),
        row=1, col=1
    )

    fig.update_layout(
        height=800,
        showlegend=False,
        title_text="Tabela de Dados do Banco de Dados",
    )

    table_html = fig.to_html(full_html=False)

    return render_template('index.html', table_html=table_html)

