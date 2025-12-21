# Flask ML Wrapper - Integração FlightOnTime

API Flask que atua como camada de integração entre a API Java (Spring Boot) e o serviço ML externo.

## Arquitetura

```
Cliente/Frontend
    ↓
API Java (Spring Boot) ← Backend Principal
    ↓ HTTP POST
API Flask (Python) ← Integration Wrapper (Este projeto)
    ↓
Serviço ML Externo ← Data Science Team
```

## Estrutura do Projeto

```
mlwrapper/
├── app/
│   ├── __init__.py                   # Flask app factory
│   ├── config.py                     # Configuration settings
│   ├── routes/
│   │   ├── __init__.py
│   │   └── prediction_routes.py     # /predict and /health endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── ml_client.py             # HTTP client for external ML service
│   └── utils/
│       ├── __init__.py
│       └── validators.py            # Validation utilities
├── tests/
│   ├── __init__.py
│   └── test_routes.py               # Unit tests
├── .env                              # Environment variables (not in git)
├── .env.example                      # Environment template
├── .gitignore                        # Git ignore rules
├── pytest.ini                        # Pytest configuration
├── README.MD                         # This file
├── requirements.txt                  # Python dependencies
└── run.py                            # Application entry point
```

## Instalação

### 1. Criar ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` baseado em `.env.example`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edite o arquivo `.env` e ajuste a variável `ML_SERVICE_URL` com a URL fornecida pela equipe de Data Science:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# External ML Service (provided by Data Science team)
ML_SERVICE_URL=http://ml-service:8000/predict
ML_SERVICE_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
```

## Execução

### Modo Desenvolvimento

```bash
python run.py
```

A API estará disponível em: `http://localhost:5000`

### Modo Produção

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker

#### Desenvolvimento local (com hot-reload)

```bash
# Subir wrapper + mock ML service
docker-compose -f docker-compose.dev.yml up

# Reconstruir se houver mudanças
docker-compose -f docker-compose.dev.yml up --build
```

#### Produção (integrado com toda aplicação)

```bash
# Do diretório raiz do projeto (FlightOnTime/)
cd ..

# Subir todos os serviços (Java API + Flask Wrapper + Mock ML)
docker-compose up -d

# Com mock ML service para testes
docker-compose --profile mock up -d

# Apenas produção (sem mock - usar ML service real)
docker-compose up -d ml-wrapper fot-api

# Ver logs
docker-compose logs -f ml-wrapper

# Parar serviços
docker-compose down
```

#### Comandos úteis Docker

```bash
# Reconstruir apenas o wrapper
docker-compose build ml-wrapper

# Rodar testes no container
docker-compose --profile test run ml-wrapper-tests

# Acessar container
docker exec -it ml-wrapper bash

# Ver logs em tempo real
docker-compose logs -f ml-wrapper
```

## Endpoints

### `POST /predict`

Predição de atraso de voo. Recebe dados do voo da API Java e retorna predição do serviço ML.

**Request:**
```json
{
  "flightNumber": "AA1234",
  "companyName": "AA",
  "flightOrigin": "JFK",
  "flightDestination": "LAX",
  "flightDepartureDate": "2025-12-20T14:30:00",
  "flightDistance": 3974
}
```

**Response:**
```json
{
  "prediction": 1,
  "probability": 0.85
}
```

- `prediction`: 0 = ON_TIME, 1 = DELAYED
- `probability`: Confiança da predição (0.0 - 1.0)

### `GET /health`

Health check do wrapper e verificação de conectividade com serviço ML externo.

**Response (UP):**
```json
{
  "status": "UP",
  "service": "Flask ML Wrapper",
  "ml_service": {
    "status": "UP",
    "ml_service": "OK"
  }
}
```

**Response (DEGRADED):**
```json
{
  "status": "DEGRADED",
  "service": "Flask ML Wrapper",
  "ml_service": {
    "status": "DOWN",
    "ml_service": "Connection refused"
  }
}
```

## Testes

### Executar testes unitários

```bash
# Rodar todos os testes
pytest

# Rodar com verbose
pytest -v

# Rodar com coverage
pytest --cov=app --cov-report=html
```

### Testes manuais

#### 1. Testar health check

```bash
curl http://localhost:5000/health
```

#### 2. Testar endpoint de predição

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "flightNumber": "AA1234",
    "companyName": "AA",
    "flightOrigin": "JFK",
    "flightDestination": "LAX",
    "flightDepartureDate": "2025-12-20T14:30:00",
    "flightDistance": 3974
  }'
```

**Windows PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:5000/health -Method Get

Invoke-RestMethod -Uri http://localhost:5000/predict -Method Post -ContentType "application/json" -Body (@{
  flightNumber = "AA1234"
  companyName = "AA"
  flightOrigin = "JFK"
  flightDestination = "LAX"
  flightDepartureDate = "2025-12-20T14:30:00"
  flightDistance = 3974
} | ConvertTo-Json)
```

### Teste de integração completa

Para testar o fluxo completo (Cliente → Java API → Flask Wrapper → ML Service):

1. **Inicie o serviço ML externo** (fornecido pela equipe de Data Science)
   ```bash
   # Porta padrão: 8000
   ```

2. **Inicie a API Flask Wrapper** (porta 5000)
   ```bash
   python run.py
   ```

3. **Inicie a API Java** (porta 8080)
   ```bash
   cd ../fot
   ./mvnw spring-boot:run  # Linux/Mac
   mvnw.cmd spring-boot:run  # Windows
   ```

4. **Faça requisição para a API Java**
   ```bash
   curl -X POST http://localhost:8080/api/v1/predict \
     -H "Content-Type: application/json" \
     -d '{
       "flightNumber": "AA1234",
       "companyName": "AA",
       "flightOrigin": "JFK",
       "flightDestination": "LAX",
       "flightDepartureDate": "2025-12-20T14:30:00",
       "flightDistance": 3974
     }'
   ```

### Teste com Mock do Serviço ML

Se o serviço ML externo ainda não estiver disponível, você pode usar um mock:

```python
# mock_ml_service.py
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    return jsonify({
        "prediction": random.randint(0, 1),
        "probability": round(random.uniform(0.5, 0.99), 2)
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "UP"})

if __name__ == '__main__':
    app.run(port=8000)
```

Execute o mock:
```bash
python mock_ml_service.py
```

## Logs

A aplicação gera logs detalhados no console:

```
2025-12-21 10:30:45 - app - INFO - Initializing Flask ML Wrapper...
2025-12-21 10:30:45 - app - INFO - ML Service configured at: http://ml-service:8000/predict
2025-12-21 10:30:45 - app - INFO - Flask ML Wrapper initialized successfully
2025-12-21 10:31:20 - app.routes.prediction_routes - INFO - Request received from Java API: AA1234
2025-12-21 10:31:20 - app.routes.prediction_routes - INFO - Forwarding to external ML service...
2025-12-21 10:31:21 - app.services.ml_client - INFO - Sending request to ML service: AA1234
2025-12-21 10:31:22 - app.services.ml_client - INFO - Prediction received from ML service: prediction=1, probability=0.85
2025-12-21 10:31:22 - app.routes.prediction_routes - INFO - Returning result to Java API: {'prediction': 1, 'probability': 0.85}
```

## Troubleshooting

### Erro: "Could not connect to ML service"

- Verifique se o serviço ML está rodando
- Confirme a URL em `.env` (`ML_SERVICE_URL`)
- Teste conectividade: `curl http://ml-service:8000/health`

### Erro: "ML service did not respond in time"

- Aumente o timeout em `.env` (`ML_SERVICE_TIMEOUT=60`)
- Verifique a performance do serviço ML

### Erro: "Empty request body"

- Certifique-se de enviar `Content-Type: application/json`
- Verifique se o body está em formato JSON válido

### Erro: "Invalid data"

- Valide os campos obrigatórios: `flightNumber`, `companyName`, `flightOrigin`, `flightDestination`, `flightDepartureDate`, `flightDistance`
- `flightDistance` deve ser maior que 0
- Códigos de aeroporto devem ter 3 letras
- Código de companhia aérea deve ter 2 letras

## Dependências

- **Flask 3.0.0** - Framework web
- **Flask-CORS 4.0.0** - CORS support
- **requests 2.31.0** - HTTP client
- **pydantic 2.5.0** - Data validation
- **python-dotenv 1.0.0** - Environment variables
- **gunicorn 21.2.0** - Production server
- **pytest 7.4.3** - Testing framework

## Responsabilidades

Este wrapper é responsável por:
- ✅ Receber requisições da API Java
- ✅ Validar dados de entrada
- ✅ Encaminhar para serviço ML externo
- ✅ Retornar resposta formatada
- ✅ Logging e monitoramento
- ✅ Health checks

**NÃO** é responsável por:
- ❌ Treinamento de modelos ML
- ❌ Lógica de negócio complexa
- ❌ Persistência de dados
- ❌ Autenticação de usuários

## Contato

Para questões sobre o serviço ML externo, entre em contato com a equipe de Data Science.
