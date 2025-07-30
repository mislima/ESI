# buscar_contratos.py
import requests
import pandas as pd
import os

def obter_dados_api(codigo_orgao, data_inicial, data_final):
    """
    Busca dados de contratos na API do Portal da Transparência,
    tratando a paginação para obter todos os resultados.

    Args:
        codigo_orgao (str): O código do órgão para a consulta.
        data_inicial (str): A data inicial no formato DD/MM/AAAA.
        data_final (str): A data final no formato DD/MM/AAAA.

    Returns:
        pandas.DataFrame: Um DataFrame com todos os contratos encontrados.
    """
    chave_api = '8313c21bd5c08c61150de8bf71adb911'
    url = "https://api.portaldatransparencia.gov.br/api-de-dados/contratos"
    headers = {"accept": "*/*", "chave-api-dados": chave_api}
    
    dados_completos = []
    pagina_atual = 1


    print(f"Buscando dados para o órgão {codigo_orgao} de {data_inicial} até {data_final}...")

    while True:
        params = {
            "codigoOrgao": codigo_orgao,
            "dataInicial": data_inicial,
            "dataFinal": data_final, 
            "pagina": pagina_atual,
            "quantidade": 100
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status() 

            dados_pagina = response.json()

            if dados_pagina:
                dados_completos.extend(dados_pagina)
                print(f"Página {pagina_atual} carregada com sucesso ({len(dados_pagina)} registros).")
                pagina_atual += 1
            else:
                print("Busca finalizada. Todas as páginas foram carregadas.")
                break
        
        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP ocorrido: {http_err} - Página: {pagina_atual}")
            print(f"Conteúdo da resposta: {response.text}")
            break
        except requests.exceptions.RequestException as req_err:
            print(f"Erro de conexão ocorrido: {req_err} - Página: {pagina_atual}")
            break
        except ValueError as json_err:
            print(f"Erro ao processar a resposta JSON: {json_err} - Página: {pagina_atual}")
            break

    return pd.DataFrame(dados_completos)

# --- Bloco principal para executar o script ---
if __name__ == '__main__':
    CODIGO_ORGAO = "25000"  # Exemplo: Ministério da Saúde
    DATA_INICIAL = "01/01/2010"
    DATA_FINAL = "31/12/2024"

    # Chamando a função com o  argumento
    df_contratos = obter_dados_api(CODIGO_ORGAO, DATA_INICIAL, DATA_FINAL)

    if not df_contratos.empty:
        print("\n--- Amostra dos Dados Obtidos ---")
        print(df_contratos.head())
        print(f"\nTotal de {len(df_contratos)} contratos encontrados.")

        # Salvando em um arquivo CSV com nome mais descritivo
        nome_arquivo = f"contratos_{CODIGO_ORGAO}_de_{DATA_INICIAL.replace('/', '-')}_a_{DATA_FINAL.replace('/', '-')}.csv"
        df_contratos.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
        print(f"\nDados salvos no arquivo: {nome_arquivo}")