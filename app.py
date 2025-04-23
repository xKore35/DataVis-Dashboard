# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 19:13:05 2025

@author: ciencia.dados1
"""
import pandas as pd 
import sqlite3
import plotly.express as px 
import dash 
import dash_bootstrap_components as dbc 
from dash import dcc, Input, Output 
from dash.dependencies import Input, Output

# CONEXÃO COM BANCO
conexao = sqlite3.connect("db/loja.db")
script = "SELECT * FROM PRODUTOS"
dados = pd.read_sql(script, conexao)

# AGRUPANDO OS DADOS  
forn_por_vlr = dados.groupby("FORNECEDOR")["VLRPROD"].sum().reset_index()
nome_por_qtd = dados.groupby("NOMEPROD")["QTDPROD"].sum().reset_index()

# CRIANDO GRÁFICOS INICIAIS
fig_forn_por_vlr = px.pie(forn_por_vlr, names="FORNECEDOR", 
                          values="VLRPROD", hole=0.5)
fig_forn_por_vlr.update_layout(template="plotly_dark")

fig_nome_por_qtd = px.bar(nome_por_qtd, x="NOMEPROD", 
                          y="QTDPROD", color="NOMEPROD")
fig_nome_por_qtd.update_layout(template="plotly_dark")

# INICIALIZANDO O APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# LAYOUT DO DASHBOARD
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id="dropdown-selecao",
                options=[{"label": i, "value": i} for i in dados["FORNECEDOR"].unique()],
                multi=True,
                clearable=False,
                className="dbc",
                style={
                    'backgroundColor': '#333',
                    'color': '#000',
                    'border': '1px solid #444',
                    'borderRadius': '5px',
                }
            )
        ),
        dbc.Col([dcc.Graph(id="fig_forn_por_qtd")], width=6),
        dbc.Col([dcc.Graph(id="fig_forn_por_vlr")], width=4),  # Gráfico de pizza
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([dcc.Graph(id="fig_nome_por_qtd")])  # Gráfico de barras por nome
    ]),

    dbc.Row(id="teste")
])

# CALLBACK PARA ATUALIZAR TODOS OS GRÁFICOS
@app.callback(
    [Output("fig_forn_por_qtd", "figure"),
     Output("fig_forn_por_vlr", "figure"),
     Output("fig_nome_por_qtd", "figure")],
    Input("dropdown-selecao", "value"),
    prevent_initial_call=True
)
def atualiza_dash(fornecedores):
    # Filtrando os dados de acordo com os fornecedores selecionados
    dados_forn = dados[dados["FORNECEDOR"].isin(fornecedores)]
    
    # Atualizando o gráfico de barras por quantidade de produto por fornecedor
    forn_por_qtd = dados_forn.groupby("FORNECEDOR")["QTDPROD"].sum().reset_index()
    fig_forn_por_qtd = px.bar(forn_por_qtd, x="FORNECEDOR", y="QTDPROD", color="FORNECEDOR")
    fig_forn_por_qtd.update_layout(template="plotly_dark")
    
    # Atualizando o gráfico de pizza por valor total por fornecedor
    forn_por_vlr = dados_forn.groupby("FORNECEDOR")["VLRPROD"].sum().reset_index()
    fig_forn_por_vlr = px.pie(forn_por_vlr, names="FORNECEDOR", values="VLRPROD", hole=0.5)
    fig_forn_por_vlr.update_layout(template="plotly_dark")
    
    # Atualizando o gráfico de barras por quantidade de produto por nome
    nome_por_qtd = dados_forn.groupby("NOMEPROD")["QTDPROD"].sum().reset_index()
    fig_nome_por_qtd = px.bar(nome_por_qtd, x="NOMEPROD", y="QTDPROD", color="NOMEPROD")
    fig_nome_por_qtd.update_layout(template="plotly_dark")
    
    # Retornando as novas figuras
    return fig_forn_por_qtd, fig_forn_por_vlr, fig_nome_por_qtd

# EXECUTANDO O APP
if __name__ == "__main__":
    app.run(debug=True)
