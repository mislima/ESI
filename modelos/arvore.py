"""
Módulo para treinamento e avaliação de um modelo de Árvore de Regressão.
"""

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

def executar_arvore(df):
    """
    Treina e avalia um modelo de Árvore de Regressão.
    """
    df = df.copy()

    #Ajuste colunas
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

    pipe = Pipeline([
        ("preprocess", preproc),
        ("regressor", DecisionTreeRegressor(random_state=42))
    ])

    X_train, X_test, y_train, y_test_arv = train_test_split(X, y, random_state=42, test_size=0.2)

    pipe.fit(X_train, y_train)
    y_pred_arv = pipe.predict(X_test)

    mse_arv = mean_squared_error(y_test_arv, y_pred_arv)
    r2_arv = r2_score(y_test_arv, y_pred_arv)

    return mse_arv, r2_arv, y_test_arv, y_pred_arv