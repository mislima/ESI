# Documentação Ágil do Projeto de Previsão de Contratos

Esta documentação simula como o projeto seria planejado e executado dentro de um framework Scrum, detalhando a visão, os épicos e as histórias de usuário que nos guiaram durante o desenvolvimento.

## Visão do Produto

O objetivo deste projeto é desenvolver um modelo de Machine Learning capaz de prever o **`valorFinalCompra`** de contratos públicos com base em suas características iniciais. O sistema visa oferecer maior previsibilidade orçamentária, identificar potenciais desvios de custos e aumentar a transparência nos processos de contratação.

## Definition of Done (DoD)

Uma história de usuário é considerada "Concluída" quando:
- O código foi escrito e está funcionando conforme o critério de aceite.
- O código possui docstrings e comentários claros.
- O código foi revisado por outro membro da equipe (Code Review).
- O código foi mesclado à branch principal (`main` ou `develop`).

---

## Product Backlog

### Épico 1: Fundação e Exploração de Dados
> *Como um Cientista de Dados, eu quero carregar, limpar e analisar os dados de contratos para entender seus padrões e prepará-los para modelagem.*

- **História de Usuário 1.1**: Criar uma função para carregar o CSV de contratos para um DataFrame do Pandas.
- **História de Usuário 1.2**: Tratar valores ausentes nas colunas críticas.
- **História de Usuário 1.3**: Converter as colunas de data em uma única coluna numérica `duracaoDias`.
- **História de Usuário 1.4**: Limpar e padronizar a coluna `compra` em uma nova coluna categórica `tipo_compra`.
- **História de Usuário 1.5**: Gerar um script (`listar_opcoes.py`) que liste todas as modalidades e tipos de compra únicos.

### Épico 2: Experimentação e Avaliação de Modelos
> *Como um Cientista de Dados, eu quero treinar e comparar diferentes algoritmos de regressão para identificar qual deles oferece a melhor performance.*

- **História de Usuário 2.1**: Implementar um pipeline de treinamento para um modelo de **Regressão Linear** e avaliar seu MSE e R².
- **História de Usuário 2.2**: Implementar um pipeline de treinamento para um modelo de **Árvore de Regressão** e avaliar seu MSE e R².
- **História de Usuário 2.3**: Implementar um pipeline de treinamento para um modelo de **Random Forest** e avaliar seu MSE e R².
- **História de Usuário 2.4**: Criar um script principal (`mainmis.py`) que execute os três modelos em sequência e imprima um resumo comparativo.

### Épico 3: Finalização e "Produção" do Modelo
> *Como um Engenheiro de ML, eu quero finalizar o modelo escolhido, criar um pipeline de treinamento robusto e salvá-lo para que possa ser usado em outras aplicações.*

- **História de Usuário 3.1**: Criar um script (`treinar_modelo.py`) dedicado a treinar o modelo **Random Forest**.
- **História de Usuário 3.2**: Construir um `Pipeline` do Scikit-learn que inclua o pré-processamento e o modelo final.
- **História de Usuário 3.3**: Salvar o pipeline treinado em um arquivo (`modelo_random_forest.joblib`).
- **História de Usuário 3.4**: Analisar e imprimir a importância das características (`feature_importances_`) do modelo final.

### Épico 4: Servir o Modelo via API
> *Como um Desenvolvedor de outra aplicação, eu quero consumir o modelo de previsão através de uma API RESTful para integrar as previsões em meu próprio sistema.*

- **História de Usuário 4.1**: Criar um endpoint de API (`POST /prever`) que receba os dados de um contrato em JSON e retorne a previsão.
- **História de Usuário 4.2**: Garantir que a API valide os tipos de dados de entrada para evitar erros.
- **História de Usuário 4.3**: Fazer com que a API carregue o modelo treinado uma única vez na inicialização.
- **História de Usuário 4.4**: Fornecer uma documentação interativa (Swagger UI) para facilitar o uso da API.
- **História de Usuário 4.5**: Formatar o valor da previsão retornado para duas casas decimais.