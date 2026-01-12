import sys
import traceback
import joblib
import pandas as pd
import numpy as np
import lightgbm as lgb
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import airportsdata
import requests

# --- 2. CONFIGURAÇÃO DO APP ---
app = Flask(__name__)
MODEL_FILE = 'flight_delay_model.pkl'
model = None

# --- 2.1 CONFIGURAÇÕES ADICIONAIS ---
#  SUBSTITUA PELA SUA CHAVE REAL
OPENWEATHER_API_KEY = "SUA_CHAVE_AQUI"
# Carrega base de dados de aeroportos (IATA -> Cidade/País)
print("--- CARREGANDO DADOS DE AEROPORTOS ---")
try:
    airports_db = airportsdata.load('IATA')
    print(f"Banco de dados carregado: {len(airports_db)} aeroportos.")
except Exception as e:
    print(f"Erro ao carregar airportsdata: {e}")
    airports_db = {}

#--- 2.2 CARREGAMENTO DO MODELO ---
print(f"--- INICIANDO SERVIDOR ---")
print(f"Tentando carregar modelo: {MODEL_FILE}")
try:
    model = joblib.load(MODEL_FILE)
    print("Modelo carregado com SUCESSO!")
except Exception as e:
    print(f"❌ ERRO CRÍTICO AO CARREGAR MODELO: {e}")
    traceback.print_exc()

# --- FUNÇÕES DE CLIMA ---
def classificar_clima(main_weather):
    """
    Mapeia o 'main' do OpenWeather para as categorias do modelo.
    Categorias do modelo: ['Good', 'Moderate', 'Severe', 'critical']
    
    Valores comuns de 'main' na OpenWeather:
    Thunderstorm, Drizzle, Rain, Snow, Mist, Smoke, Haze, Dust, Fog, Sand, Ash, Squall, Tornado, Clear, Clouds
    """
    if not main_weather:
        return 'Good'
        
    main_weather = main_weather.lower()
    
    # 1. Critical: Tempestades violentas e eventos extremos
    if main_weather in ['thunderstorm', 'tornado', 'squall', 'ash']:
        return 'critical'
        
    # 2. Severe: Neve e visibilidade severamente reduzida (Areia/Poeira)
    elif main_weather in ['snow', 'sand', 'dust']:
        return 'Severe'
        
    # 3. Moderate: Chuva, Garoa e Visibilidade reduzida (Neblina)
    elif main_weather in ['rain', 'drizzle', 'mist', 'fog', 'haze', 'smoke']:
        return 'Moderate'
        
    # 4. Good: Céu limpo ou nublado (sem precipitação)
    elif main_weather in ['clear', 'clouds']:
        return 'Good'
        
    # Padrão de segurança
    return 'Good'

def consultar_clima(iata_code, data_iso):
    """
    Adaptação para Plano Gratuito:
    - Passado: Retorna 'Good' (API bloqueada).
    - Futuro (>5 dias): Retorna 'Good' (Limite da API).
    - Futuro (<=5 dias): Consulta API Forecast.
    """
    if iata_code not in airports_db:
        return 'Good', 'Aeroporto desconhecido'

    airport = airports_db[iata_code]
    lat, lon = airport['lat'], airport['lon']
    
    try:
        target_date = pd.to_datetime(data_iso)
        now = datetime.now()
        target_timestamp = int(target_date.timestamp())
    except:
        return 'Good', 'Erro na data'

    # --- Logica Consulta API ---

    if target_date < now:
        # PLANO FREE NÃO TEM HISTÓRICO.
        # Não chamamos a API para evitar erro 401.
        print(f"Data no passado ({target_date}). Plano gratuito não permite histórico. Usando padrão.")
        return 'Good', 'Sem Histórico (Plano Gratuito)'
    
    elif target_date > now + timedelta(days=5):
        print(f"Data muito distante ({target_date}). Limite é 5 dias.")
        return 'Good', 'Data excede limite 5 dias'
    
    else:
        # PREVISÃO (Disponível no Free)
        url = (f"https://api.openweathermap.org/data/2.5/forecast"
               f"?lat={lat}&lon={lon}"
               f"&appid={OPENWEATHER_API_KEY}")
        
        print(f"Consultando Previsão: {iata_code} em {target_date}...")

        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            if response.status_code != 200:
                msg = data.get('message', 'Erro desconhecido')
                print(f"   -> Erro API: {msg}")
                return 'Good', f"Erro API: {msg}"

            # Procura o horário mais próximo na lista de 3 em 3 horas
            lista_previsoes = data.get('list', [])
            weather_main = None
            melhor_dif = float('inf')

            for item in lista_previsoes:
                dt_item = int(item['dt'])
                dif = abs(dt_item - target_timestamp)
                
                if dif < melhor_dif:
                    melhor_dif = dif
                    weather_main = item['weather'][0]['main']
                
                # Se a diferença for menor que 90 min, é o slot perfeito
                if dif < 5400: 
                    break
            
            if weather_main:
                cat = classificar_clima(weather_main)
                print(f"   -> Previsão: '{weather_main}' -> '{cat}'")
                return cat, weather_main
            
            return 'Good', 'Sem dados correspondentes'

        except Exception as e:
            print(f"   -> Exceção: {e}")
            return 'Good', 'Erro Conexão'

# --- 3. ENDPOINT HEALTH (Blindado contra erros 500) ---

@app.route('/health', methods=['GET'])
def health():
    try:
       
        model_obj = globals().get('model')
        is_up = model_obj is not None

        status_data = {
            "status": "UP" if is_up else "DOWN",
            "service": "modelos-ml",
            "model_loaded": is_up
        }

        code = 200 if is_up else 503

        print(f"Health check: {code} - {status_data}")
        return jsonify(status_data), code

    except Exception as e:
        print(f"ERRO NO HEALTH CHECK: {e}")
        traceback.print_exc()
        return jsonify({'status': 'ERROR', 'message': str(e)}), 500

# --- 4. ENDPOINT PREDICT (Com validação solicitada) ---


@app.route('/predict', methods=['POST'])
def predict():
    # Verifica modelo
    current_model = globals().get('model')
    if current_model is None:
        return jsonify({'message': 'Modelo offline - falha no carregamento', 'status': 'error'}), 503

    try:
        data_json = request.get_json()
        if not data_json:
            return jsonify({'status': 'error', 'message': 'JSON vazio.'}), 400


# Aceita tanto os nomes antigos quanto os novos (padrão IATA)
        origem = data_json.get('sg_iata_origem') or data_json.get('origem')
        destino = data_json.get('sg_iata_destino') or data_json.get('destino')
        data_str = data_json.get('dt_partida_prevista') or data_json.get('data_partida')
       
        if not all([origem, destino, data_str]):
            return jsonify({'message': 'Faltam campos obrigatórios'}), 400

        weather_cat, weather_main = consultar_clima(origem, data_str)

        # 2. Feature Engineering
        try:
            dt_obj = pd.to_datetime(data_str)
        except:
            return jsonify({'message': 'Formato de data inválido'}), 400

        features = {
            'Month': int(dt_obj.month),
            'DayOfWeek': int(dt_obj.dayofweek) + 1,
            'DepTime': float(dt_obj.hour * 100 + dt_obj.minute),
            'Origin': str(origem),
            'Dest': str(destino),
            'weather_category': str(weather_cat)
        }

        # Cria DataFrame
        df_input = pd.DataFrame([features])
        
        # Conversão obrigatória para category (LightGBM)
        for col in ['Origin', 'Dest', 'weather_category']:
            df_input[col] = df_input[col].astype('category')

        # Previsão
        prediction = current_model.predict(df_input)[0]

        proba = 0.0

        try:
            proba = float(current_model.predict_proba(df_input)[0][1])
        except:
            pass

        return jsonify({
            'prediction': int(prediction),
            'label': "Delayed" if prediction == 1 else "On Time",
            'probability_delay': proba,
            'weather_context': {
                'main': weather_main,
                'category_used': weather_cat,
                'source': 'OpenWeatherMap (Main Field)'
            },
            'status': 'success'
        })

    except Exception as e:
        print("Erro durante o processamento da previsão:")
        traceback.print_exc()
        return jsonify({'message': str(e), 'status': 'error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
