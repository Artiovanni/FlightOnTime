import requests
import random
import json
import time
from datetime import datetime, timedelta

# --- CONFIGURAÇÕES ---
URL_API = "http://localhost:5000/predict"
QTD_TESTES = 5  # Quantas previsões você quer gerar?

# Lista de aeroportos para variar os testes (IATA)
AEROPORTOS = [
    'GRU', 'CGH', 'GIG', 'SDU', 'CNF', 'BSB',  # Brasil
    'MIA', 'JFK', 'LIS', 'LHR', 'MAD', 'CDG'   # Internacionais
]

def gerar_data_valida_openweather():
    """
    Gera uma data aleatória entre AGORA e DAQUI A 4 DIAS.
    Motivo: O plano gratuito da OpenWeather só aceita previsões de até 5 dias.
    """
    agora = datetime.now()
    # Adiciona entre 1 hora e 4 dias (96 horas) para frente
    horas_random = random.randint(1, 96) 
    minutos_random = random.randint(0, 59)
    
    data_futura = agora + timedelta(hours=horas_random, minutes=minutos_random)
    return data_futura.strftime("%Y-%m-%d %H:%M:%S")

def executar_teste(index):
    # Escolhe origem e destino aleatórios (garantindo que não sejam iguais)
    origem = random.choice(AEROPORTOS)
    destino = random.choice(AEROPORTOS)
    while destino == origem:
        destino = random.choice(AEROPORTOS)

    payload = {
        "sg_iata_origem": origem,
        "sg_iata_destino": destino,
        "dt_partida_prevista": gerar_data_valida_openweather()
    }

    print(f"\n✈️  TESTE #{index + 1} --------------------------------")
    print(f"Envio: {payload['sg_iata_origem']} -> {payload['sg_iata_destino']} | Data: {payload['dt_partida_prevista']}")

    try:
        start_time = time.time()
        response = requests.post(URL_API, json=payload)
        end_time = time.time()

        if response.status_code == 200:
            dados = response.json()
            tempo_resp = round((end_time - start_time) * 1000, 2)
            
            # Extraindo dados para exibição limpa
            label = dados.get('label', 'N/A')
            prob = dados.get('probability_delay', 0.0)
            clima = dados.get('weather_context', {})
            desc_clima = clima.get('main', 'N/A')
            cat_clima = clima.get('category_used', 'N/A')

            print(f"✅ Status: 200 OK ({tempo_resp}ms)")
            print(f"   -> Previsão: {label} (Probabilidade de Atraso: {prob:.2%})")
            print(f"   -> Clima Real: '{desc_clima}' (Classificado como: {cat_clima})")
        else:
            print(f"⚠️ Erro {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não foi possível conectar ao servidor. Verifique se 'python app.py' está rodando.")

if __name__ == "__main__":
    print(f"Iniciando {QTD_TESTES} testes automáticos...")
    print("Nota: As datas estão restritas aos próximos 4 dias para compatibilidade com o Plano Free.")
    
    for i in range(QTD_TESTES):
        executar_teste(i)
        time.sleep(1) # Pausa de 1s entre requisições para não bloquear a API
    
    print("\n🏁 Testes finalizados.")