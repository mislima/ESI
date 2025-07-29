
"""
Script da API para servir o modelo de previsão de valor de contrato.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

#CARREGAMENTO DO MODELO ---
CAMINHO_ATUAL = Path(__file__)
PASTA_RAIZ = CAMINHO_ATUAL.parent.parent
CAMINHO_MODELO = PASTA_RAIZ / "modelo_random_forest.joblib"

try:
    pipeline_carregado = joblib.load(CAMINHO_MODELO)
    print(f"Modelo treinado carregado com sucesso de: {CAMINHO_MODELO}")
except FileNotFoundError:
    print(f"Erro: Arquivo de modelo não encontrado em '{CAMINHO_MODELO}'. Execute o script 'treinar_modelo.py' primeiro.")
    pipeline_carregado = None


app = FastAPI(
    title="API de Precificação de Contratos",
    description="Use esta API para prever o valor final de uma compra com base em seus dados.",
    version="3.1.0" 
)

class DadosContrato(BaseModel):
    """
    Define o schema de dados para uma requisição de previsão.
    """
    valorInicialCompra: float
    modalidadeCompra: str
    tipo_compra: str
    situacaoContrato: str
    duracaoDias: int

    class Config:
        json_schema_extra = {
            "example": {
                "valorInicialCompra": 50000.0,
                "modalidadeCompra": "Pregao",
                "tipo_compra": "Serviço",
                "situacaoContrato": "Ativo",
                "duracaoDias": 365
            }
        }

@app.get("/")
def home():
    """Endpoint raiz para verificar se a API está operacional."""
    return {"status": "API de previsão está no ar. Acesse /docs para a documentação."}

@app.post("/prever")
def prever_valor_final(dados: DadosContrato):
    """
    Recebe os dados de um contrato e retorna o valor final previsto.
    """
    if pipeline_carregado is None:
        raise HTTPException(status_code=503, detail="Modelo não está carregado. Verifique os logs do servidor.")

    try:
        dados_df = pd.DataFrame([dados.dict()])
        previsao = pipeline_carregado.predict(dados_df)
        valor_previsto = previsao[0]

        # Arredondamos o valor para 2 casas decimais
        valor_arredondado = round(valor_previsto, 2)

        return {"valorFinalCompra_previsto": valor_arredondado}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro durante a previsão: {str(e)}")