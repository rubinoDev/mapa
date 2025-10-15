# Mapa de Calor: Casos de Hipertensão e Diabetes em SP

Este é um aplicativo web interativo que visualiza a densidade de casos de diabetes e hipertensão nos municípios do estado de São Paulo.

O aplicativo utiliza a biblioteca Streamlit para criar a interface web, Pandas para a manipulação dos dados e Folium para a geração do mapa de calor interativo.

## Funcionalidades

- Visualização de dados de saúde em um mapa de calor geográfico.
- Interface web interativa e fácil de usar.
- Combinação de dados locais (`hipertensao_diabetes.csv`) com dados geográficos de uma fonte externa.

## Pré-requisitos

- Python 3.8 ou superior

## Instalação

1.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  **Instale as dependências necessárias:**
    ```bash
    pip install -r requirements.txt
    ```

## Como Usar

1.  Certifique-se de que o arquivo `hipertensao_diabetes.csv` está no mesmo diretório que o script.

2.  Execute o aplicativo Streamlit a partir do seu terminal:
    ```bash
    streamlit run mapa_diabetes_hipertensao.py
    ```

3.  Após executar o comando, o aplicativo será aberto automaticamente no seu navegador web padrão.

## Fontes de Dados

-   **Dados de Saúde:** `hipertensao_diabetes.csv` (arquivo local).
-   **Dados Geográficos:** [Municipios-Brasileiros](https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv) - um arquivo CSV contendo os códigos IBGE, latitude e longitude dos municípios brasileiros.
