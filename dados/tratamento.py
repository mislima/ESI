
"""
Módulo central para carregamento, limpeza e engenharia de características.
"""

import pandas as pd
import ast

def carregar_dados(caminho_csv):
    """
    Carrega os dados e realiza a extração e simplificação das categorias de compra.
    """
    df = pd.read_csv(caminho_csv)

    #Extrair a descrição do objeto ---
    def extrair_objeto(valor_celula):
        try:
            dict_valor = ast.literal_eval(str(valor_celula))
            if isinstance(dict_valor, dict) and 'objeto' in dict_valor:
                return dict_valor['objeto']
        except (ValueError, SyntaxError):
            return str(valor_celula)
        return "NaoIdentificado"

    df['compra_descricao'] = df['compra'].apply(extrair_objeto)
    
    #Simplificar a descrição em categorias usando palavras-chave
    def simplificar_categoria_compra(descricao):
        texto = str(descricao).lower() 
        
       
        if 'serviço' in texto or 'serviços' in texto:
            return 'Serviço'
        if 'material' in texto or 'fornecimento' in texto or 'aquisição' in texto or 'itens' in texto:
            return 'Material_Fornecimento'
        if 'obra' in texto or 'empreita' in texto or 'engenharia' in texto:
            return 'Obra_Engenharia'
        if 'locação' in texto or 'aluguel' in texto:
            return 'Locação'
        if 'consultoria' in texto:
            return 'Consultoria'
        if 'software' in texto or 'sistema' in texto or 'ti' in texto or 'licença' in texto:
            return 'TI_Software'
        
        return 'Outros' 

    print("Criando categorias simplificadas a partir das descrições...")

    # Cria a nova coluna 'tipo_compra' baseada na descrição extraída
    df['tipo_compra'] = df['compra_descricao'].apply(simplificar_categoria_compra)
    print("✅ Nova coluna 'tipo_compra' criada.")
    

    df['dataAssinatura'] = pd.to_datetime(df['dataAssinatura'], errors='coerce')
    df['dataFimVigencia'] = pd.to_datetime(df['dataFimVigencia'], errors='coerce')
    df['duracaoDias'] = (df['dataFimVigencia'] - df['dataAssinatura']).dt.days
    df = df[df['valorFinalCompra'] >= 0]

    return df