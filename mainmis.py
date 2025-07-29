"""
Script principal para experimentação e comparação de modelos de regressão.

Este módulo orquestra a execução de diferentes algoritmos de Machine Learning
(Regressão Linear, Árvore de Regressão e Random Forest) para prever o valor
final de contratos. Ele carrega os dados, executa cada modelo e imprime as
métricas de avaliação (MSE e R²) para permitir uma comparação direta de performance.

Nota: Este script depende de implementações específicas nos módulos:
- `dados.tratamento` para o carregamento e pré-processamento dos dados.
- `modelos.*` para a execução de cada modelo individual.
"""

from dados.tratamento import carregar_dados
from modelos.regressaoLinear import executar_regressao_linear
from modelos.arvore import executar_arvore
from modelos.randomForest import executar_random_forest



def main():
    """
    Função principal que coordena o fluxo de execução e comparação dos modelos.
    """
    print("Carregando dados...")
    df = carregar_dados("contratos_25000_de_01-01-2010_a_31-12-2024.csv")

    print("\n--- Regressão Linear ---")
    mse_lr, r2_lr, y_test_lr, y_pred_lr = executar_regressao_linear(df)
    print(f"MSE: {mse_lr:.2f}, R²: {r2_lr:.4f}")

    print("\n--- Árvore de Regressão ---")
    mse_arv, r2_arv, y_test_arv, y_pred_arv = executar_arvore(df)
    print(f"MSE: {mse_arv:.2f}, R²: {r2_arv:.4f}")

    print("\n--- Random Forest ---")
    mse_rf, r2_rf, y_test_rf, y_pred_rf = executar_random_forest(df)
    print(f"MSE: {mse_rf:.2f}, R²: {r2_rf:.4f}")

if __name__ == "__main__":
    main()