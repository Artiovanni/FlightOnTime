import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Configuração da Página
st.set_page_config(page_title="FlightOnTime - Previsão de Atrasos", page_icon="✈️")

# Título e Estilo
st.title("✈️ FlightOnTime")
st.markdown("Previsão de atrasos de voos com base em **IA** e **Clima em Tempo Real**.")

# --- SIDEBAR (Entradas) ---
st.sidebar.header("Dados do Voo")

# Lista de Aeroportos (Exemplo)
aeroportos = ['GRU', 'CGH', 'GIG', 'SDU', 'CNF', 'BSB', 'MIA', 'JFK', 'LIS', 'LHR', 'MAD', 'CDG']

origem = st.sidebar.selectbox("Aeroporto de Origem (IATA)", aeroportos, index=0)
destino = st.sidebar.selectbox("Aeroporto de Destino (IATA)", aeroportos, index=2)

# Data e Hora
data_hoje = datetime.now()
data_selecionada = st.sidebar.date_input("Data da Partida", data_hoje)
hora_selecionada = st.sidebar.time_input("Hora da Partida", datetime.now().time())

# Combinar data e hora
data_completa = datetime.combine(data_selecionada, hora_selecionada)
data_str = data_completa.strftime("%Y-%m-%d %H:%M:%S")

# Botão de Previsão
if st.sidebar.button("Realizar Previsão"):
    
    if origem == destino:
        st.error("A origem e o destino não podem ser iguais!")
    else:
        # Preparar Payload
        payload = {
            "sg_iata_origem": origem,
            "sg_iata_destino": destino,
            "dt_partida_prevista": data_str
        }

        # URL da sua API Flask
        url = "http://localhost:5000/predict"

        with st.spinner('Consultando satélites e processando modelo...'):
            try:
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    dados = response.json()
                    
                    # --- EXIBIÇÃO DOS RESULTADOS ---
                    col1, col2 = st.columns(2)
                    
                    prediction = dados.get('prediction')
                    label = dados.get('label')
                    prob = dados.get('probability_delay', 0)
                    weather = dados.get('weather_context', {})
                    
                    with col1:
                        st.subheader("Resultado da IA")
                        if prediction == 1:
                            st.error(f"⚠️ {label} (Atraso Provável)")
                        else:
                            st.success(f"✅ {label} (No Horário)")
                        
                        st.metric("Probabilidade de Atraso", f"{prob:.2%}")

                    with col2:
                        st.subheader("Condições Climáticas")
                        main_weather = weather.get('main', 'N/A')
                        category = weather.get('category_used', 'N/A')
                        
                        # Ícone baseado no clima
                        icone = "🌤️"
                        if category == 'Moderate': icone = "🌧️"
                        if category == 'Severe': icone = "⛈️"
                        if category == 'critical': icone = "🌪️"
                        
                        st.info(f"{icone} Clima: **{main_weather}**")
                        st.caption(f"Classificação do Modelo: {category}")
                        st.caption(f"Fonte: {weather.get('source', 'N/A')}")
                    
                    # Detalhes técnicos (Expander)
                    with st.expander("Ver JSON de Resposta"):
                        st.json(dados)

                else:
                    st.error(f"Erro na API: {response.status_code}")
            
            except requests.exceptions.ConnectionError:
                st.error("Não foi possível conectar ao servidor Flask. Verifique se ele está rodando.")