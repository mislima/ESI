"""
Módulo para treinamento e avaliação de um modelo de Regressão Linear.

Este script contém a função `executar_regressao_linear`, que encapsula todo o
processo de preparação de dados, treinamento e avaliação de um modelo
LinearRegression do Scikit-learn. É projetado para ser chamado por um script
orquestrador (como `mainmis.py`) para fins de comparação com outros modelos.
"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

def executar_regressao_linear(df):
    """
    Treina e avalia um modelo de Regressão Linear.

    Esta função realiza o pré-processamento dos dados, incluindo o tratamento de
    valores ausentes e a codificação de variáveis categóricas, antes de treinar
    o modelo.

    Args:
        df (pd.DataFrame): O DataFrame contendo os dados brutos dos contratos.

    Returns:
        tuple: Uma tupla contendo:
            - mse_rl (float): O Erro Quadrático Médio (Mean Squared Error) do modelo.
            - r2_rl (float): O coeficiente de determinação (R²) do modelo.
            - y_test_rl (pd.Series): Os valores reais do alvo no conjunto de teste.
            - y_pred_rl (np.array): Os valores previstos pelo modelo para o conjunto de teste.
    """
    df = df.copy()

    #Ajuste de colunas
    df['duracaoDias'] = df['duracaoDias'].fillna(df['duracaoDias'].mean())
    for col in ['modalidadeCompra', 'compra', 'situacaoContrato']:
        df[col] = df[col].fillna("NaoInformado")

    df = df[['valorInicialCompra', 'modalidadeCompra', 'compra', 'situacaoContrato', 'duracaoDias', 'valorFinalCompra']].dropna()

    X = df.drop("valorFinalCompra", axis=1)
    y = df["valorFinalCompra"]

    categ = ['modalidadeCompra', 'compra', 'situacaoContrato']
    preproc = ColumnTransformer([
        ("onehot", OneHotEncoder(drop="first", handle_unknown="ignore"), categ)
    ], remainder='passthrough')

    pipe_rl = Pipeline([
        ("preprocess", preproc),
        ("regressor", LinearRegression())
    ])

    X_train, X_test, y_train, y_test_rl = train_test_split(X, y, random_state=42, test_size=0.2)

    pipe_rl.fit(X_train, y_train)
    y_pred_rl = pipe_rl.predict(X_test)

    mse_rl = mean_squared_error(y_test_rl, y_pred_rl)
    r2_rl = r2_score(y_test_rl, y_pred_rl)

    return mse_rl, r2_rl, y_test_rl, y_pred_rl