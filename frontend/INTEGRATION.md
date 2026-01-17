# 🎨 Frontend - FlightOnTime

Interface web para consulta de previsões de atraso de voos.

## 🚀 Como Rodar

### Opção 1: Com Docker (Recomendado)

Na raiz do projeto:

```bash
# Subir todos os serviços incluindo o frontend
docker compose up -d

# Acessar
# Frontend: http://localhost:3000
# Backend API: http://localhost:8080
# Swagger: http://localhost:8080/swagger-ui.html
```

O frontend estará disponível em **<http://localhost:3000>**

### Opção 2: Servidor Local

Se preferir rodar apenas o frontend localmente:

#### Usando Python

```bash
cd frontend
python -m http.server 3000
```

#### Usando Node.js

```bash
cd frontend
npx http-server -p 3000
```

#### Usando PHP

```bash
cd frontend
php -S localhost:3000
```

**Importante:** Com servidor local, você precisa ter o backend rodando em `http://localhost:8080`

## 📋 Funcionalidades

- ✅ Formulário completo de consulta de voos
- ✅ Integração com API REST do backend
- ✅ Visualização em gauge (velocímetro) da probabilidade
- ✅ Feedback visual com cores (Verde/Laranja/Vermelho)
- ✅ Responsivo para mobile e desktop
- ✅ Animações suaves de entrada

## 🛠️ Tecnologias

- HTML5
- CSS3 (Custom Properties, Flexbox, Grid)
- JavaScript (ES6+, Fetch API)
- Nginx (quando rodado no Docker)

## 📝 Campos do Formulário

- **Número do Voo**: Ex: LA4001
- **Companhia Aérea**: LA (LATAM), AD (Azul), G3 (Gol)
- **Origem**: Código IATA do aeroporto (Ex: GRU)
- **Destino**: Código IATA do aeroporto (Ex: GIG)
- **Data**: Data do voo
- **Horário**: Hora de partida prevista
- **Distância**: Distância em km entre origem e destino

## 🔄 Integração com API

O frontend consome o endpoint:

```text
POST /api/v1/predict
```

**Request:**

```json
{
  "flightNumber": "LA4001",
  "companyName": "LA",
  "flightOrigin": "GRU",
  "flightDestination": "GIG",
  "flightDepartureDate": "2025-12-31T14:30:00",
  "flightDistance": 358
}
```

**Response:**

```json
{
  "prediction": "DELAYED",
  "probability": 0.78,
  "confidenceLevel": "HIGH",
  "probabilityPercentage": 78.0,
  "formattedProbability": "78.00%",
  "summary": "Flight is predicted to be DELAYED with HIGH confidence (78.00%)"
}
```

## 🎨 Estrutura de Arquivos

```text
frontend/
├── index.html          # Página principal
├── ajuda.html          # Página de ajuda
├── style.css           # Estilos globais
├── script.js           # Lógica de integração com API
├── Dockerfile          # Imagem Docker com Nginx
├── nginx.conf          # Configuração do Nginx
└── README.md           # Documentação
```

## 🐛 Troubleshooting

### Erro de CORS

Se estiver rodando o frontend localmente (fora do Docker), você pode ter problemas de CORS. Soluções:

1. **Use o Docker** (recomendado) - o nginx já está configurado como proxy
2. Configure CORS no backend
3. Use uma extensão de navegador para desabilitar CORS (apenas desenvolvimento)

### API não responde

Verifique se os containers estão rodando:

```bash
docker compose ps
```

Verifique logs:

```bash
docker compose logs fot-api
docker compose logs frontend
```

## 📱 Compatibilidade

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

---

**Desenvolvido por Los Hermanos** 🚀
