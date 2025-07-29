import pandas as pd

"""
Utilitário para extrair e listar os valores únicos de colunas específicas.

Este script foi criado para auxiliar desenvolvedores e analistas a identificarem
rapidamente todas as categorias possíveis em colunas como 'compra' e
'modalidadeCompra' do dataset de contratos.

A saída pode ser usada para popular menus dropdown em uma interface de usuário
ou para validar entradas em um sistema de previsão.
"""

caminho_csv = "contratos_25000_de_01-01-2010_a_31-12-2024.csv"

try:
    # Carregar os dados
    df = pd.read_csv(caminho_csv)

    # Obter os valores únicos e tratar valores ausentes como "NaoInformado"
    opcoes_compra = df['compra'].fillna("NaoInformado").unique()
    opcoes_modalidade = df['modalidadeCompra'].fillna("NaoInformado").unique()

    # Ordenar as listas para facilitar a visualização
    opcoes_compra.sort()
    opcoes_modalidade.sort()

    # Imprimir as listas de forma organizada
    print("\n Opções encontradas com sucesso!")
    print("\n--- Opções para o campo 'compra' ---")
    print(opcoes_compra.tolist())

    print("\n--- Opções para o campo 'modalidadeCompra' ---")
    print(opcoes_modalidade.tolist())

except FileNotFoundError:
    print(f"\n ERRO: O arquivo CSV não foi encontrado.")
    print(f"Verifique se o caminho no script ('{caminho_csv}') está correto e se o arquivo está na pasta certa.")
except KeyError as e:
    print(f" ERRO: A coluna {e} não foi encontrada no arquivo CSV.")
    print("Por favor, verifique os nomes das colunas no seu arquivo.")