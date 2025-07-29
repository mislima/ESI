# Projeto de Previsão de Valor Final de Contratos Públicos

##  Visão Geral

Este projeto utiliza técnicas de Machine Learning para prever o valor final de contratos (`valorFinalCompra`) com base em dados históricos. O objetivo é fornecer uma ferramenta para análise de custos, planejamento orçamentário e identificação de anomalias em processos de licitação.

O sistema completo inclui desde o tratamento dos dados e treinamento do modelo até a sua exposição através de uma API RESTful. O modelo final escolhido foi um **Random Forest Regressor**.

##  Funcionalidades

- **Tratamento de Dados**: Carrega, limpa e realiza engenharia de características nos dados brutos de contratos.
- **Experimentação**: Scripts para treinar e comparar diferentes modelos de regressão (Linear, Árvore, Random Forest).
- **Treinamento Final**: Um pipeline robusto para treinar o modelo campeão (Random Forest) e salvá-lo em um arquivo `.joblib`.
- **API de Previsão**: Uma API web criada com FastAPI para servir o modelo, recebendo dados de um contrato e retornando a previsão em tempo real.
- **Utilitários**: Scripts para listar as opções de entrada válidas, facilitando a integração.

##  Estrutura do Projeto

├── api/
│   └── main.py                 # Script da API FastAPI para servir o modelo
├── dados/
│   └── tratamento.py             # Módulo para carregar e tratar os dados
├── modelos/
│   ├── arvore.py                 # Script para executar Árvore de Regressão (experimental)
│   ├── randomForest.py           # Script para executar Random Forest (experimental)
│   └── regressaoLinear.py        # Script para executar Regressão Linear (experimental)
├── DOCUMENTACAO_AGIL.md          # Documentação do projeto no formato Scrum
├── README.md                     # Este arquivo
├── listar_opcoes.py              # Utilitário para listar valores únicos das colunas
├── mainmis.py                    # Script principal para comparar os modelos experimentais
├── treinar_modelo.py             # Script para treinar e salvar o modelo final
├── requirements.txt              # Lista de dependências do projeto
└── modelo_random_forest.joblib   # (Gerado por treinar_modelo.py)

##  Pré-requisitos

- Python 3.8+
- Bibliotecas listadas no `requirements.txt`

##  Instalação

1.  Navegue até a pasta do projeto no seu terminal.

2.  Crie e ative um ambiente virtual (recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

##  Uso do Projeto

O fluxo de trabalho recomendado é:

**1. Treinar o Modelo Final**

Execute este script para processar os dados, treinar o modelo Random Forest e salvar o arquivo `modelo_random_forest.joblib`. **Lembre-se de ter o seu arquivo CSV de dados na pasta principal.**
```bash
python treinar_modelo.py