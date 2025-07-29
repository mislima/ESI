

"""
Script para treinamento e serialização do modelo final de produção.

Este script executa os seguintes passos:
1.  Carrega os dados de contratos utilizando a função de tratamento.
2.  Seleciona as características (`features`) finais para o treinamento.
3.  Define um pipeline de pré-processamento e modelagem utilizando
    `ColumnTransformer` para variáveis categóricas e `RandomForestRegressor`
    como o estimador.
4.  Treina o pipeline completo com todos os dados preparados.
5.  Salva (serializa) o objeto do pipeline treinado em um arquivo `.joblib`.
6.  Analisa e imprime a importância das características do modelo treinado.

O artefato final ('modelo_random_forest.joblib') é o modelo pronto para ser
usado em produção para fazer previsões em novos dados.
"""

import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

from dados.tratamento import carregar_dados

print("Iniciando o processo de treinamento...")


#Esta função cria a coluna 'tipo_compra'
df = carregar_dados("contratos_25000_de_01-01-2010_a_31-12-2024.csv")

#Preparar os dados para o modelo
print("Selecionando as colunas finais para o modelo...")

#Selecionamos APENAS as colunas que queremos.
colunas_para_o_modelo = [
    'valorInicialCompra',
    'modalidadeCompra',
    'tipo_compra', # A nova coluna limpa
    'situacaoContrato',
    'duracaoDias',
    'valorFinalCompra'
]
df_modelo = df[colunas_para_o_modelo].dropna()

#Separa as características X do alvo y
X = df_modelo.drop("valorFinalCompra", axis=1)
y = df_modelo["valorFinalCompra"]

#Cria o Pipeline completo
print("Criando o pipeline de pré-processamento e o modelo...")

#Define quais das colunas selecionadas são categóricas
categ = ['modalidadeCompra', 'tipo_compra', 'situacaoContrato']

preproc = ColumnTransformer([
    ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore"), categ)
], remainder='passthrough')

pipeline_final = Pipeline([
    ("preprocess", preproc),
    ("regressor", RandomForestRegressor(random_state=42))
])

#Treina o Pipeline
print("Treinando o modelo...")
pipeline_final.fit(X, y)

#Salva o Pipeline
print("\nSalvando o pipeline treinado no arquivo 'modelo_random_forest.joblib'...")
# Esta ação irá sobrescrever o modelo antigo e problemático
joblib.dump(pipeline_final, 'modelo_random_forest.joblib')
print("✅ Modelo salvo com sucesso!")


#Análise de Importância
print("\n--- Importância das Características (Modelo Final) ---")
modelo_rf = pipeline_final.named_steps['regressor']
preprocessador = pipeline_final.named_steps['preprocess']
nomes_categoricos = preprocessador.named_transformers_['onehot'].get_feature_names_out(categ)
nomes_numericos = [col for col in X.columns if col not in categ]
todos_os_nomes = np.concatenate([nomes_categoricos, nomes_numericos])
importancias = pd.DataFrame({
    'Característica': todos_os_nomes,
    'Importância': modelo_rf.feature_importances_
}).sort_values(by='Importância', ascending=False)
print(importancias)