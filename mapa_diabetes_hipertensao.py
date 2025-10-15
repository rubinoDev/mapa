import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import requests
import io

st.set_page_config(layout="wide")
st.title("Mapa de Calor - Casos de Diabetes e Hipertensão em SP")

st.markdown("""
Este aplicativo visualiza a densidade de casos de **diabetes e hipertensão** nos municípios do estado de São Paulo.
Os dados são carregados, combinados com coordenadas geográficas e exibidos como um mapa de calor interativo.
""")

# URL para o dataset de municípios com coordenadas
GEO_DATA_URL = "https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv"

@st.cache_data
def load_data(file_path):
    # Carregar dados de diabetes e hipertensão, pulando o cabeçalho
    df = pd.read_csv(file_path, sep=';', skiprows=25, encoding='latin1')

    # O cabeçalho do CSV tem um ';' extra no final, o que cria uma coluna vazia.
    # Definir os nomes das colunas manualmente para evitar erros de parsing.
    df.columns = ['Uf', 'Ibge', 'Municipio', 'Diabetes', 'Hipertensao_arterial', 'Vazio']
    df = df.drop(columns=['Vazio'])

    df = df.dropna(subset=['Ibge'])
    df['Ibge'] = df['Ibge'].astype(int)
    
    # Limpar e converter colunas numéricas
    for col in ['Diabetes', 'Hipertensao_arterial']:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace('.', '', regex=False), errors='coerce')
    
    df = df.dropna(subset=['Diabetes', 'Hipertensao_arterial'])
    
    df['Total_Casos'] = df['Diabetes'] + df['Hipertensao_arterial']
    return df

@st.cache_data
def get_geo_data():
    # Obter dados geográficos dos municípios
    response = requests.get(GEO_DATA_URL)
    response.raise_for_status()
    geo_df = pd.read_csv(io.StringIO(response.text))
    # Apenas municípios de SP, usando o código da UF (35 para SP)
    geo_df_sp = geo_df[geo_df['codigo_uf'] == 35].copy()
    geo_df_sp.rename(columns={'codigo_ibge': 'Ibge'}, inplace=True)
    return geo_df_sp[['Ibge', 'latitude', 'longitude']]

try:
    health_df = load_data('hipertensao_diabetes.csv')
    geo_df = get_geo_data()

    # Unir os dados de saúde com os dados geográficos
    merged_df = pd.merge(health_df, geo_df, on='Ibge')

    # Remover quaisquer linhas sem coordenadas para evitar erros no mapa
    merged_df.dropna(subset=['latitude', 'longitude'], inplace=True)

    st.subheader("🔍 Pré-visualização dos Dados Combinados")
    st.dataframe(merged_df.head())

    # ---------- MAPA DE CALOR ----------
    map_center = [merged_df['latitude'].mean(), merged_df['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=7)

    # Criar dados para o mapa de calor
    heat_data = [[row['latitude'], row['longitude'], row['Total_Casos']] for index, row in merged_df.iterrows()]

    # Adicionar o mapa de calor
    HeatMap(heat_data, radius=15).add_to(m)

    st.subheader("🗺️ Mapa de Calor da Densidade de Casos")
    st_folium(m, width=1000, height=600)

except FileNotFoundError:
    st.error("Arquivo 'hipertensao_diabetes.csv' não encontrado. Por favor, faça o upload do arquivo.")
except Exception as e:
    st.error(f"Ocorreu um erro ao processar os dados: {e}")
