# Guia de Desenvolvimento - FlightOnTime

## 🎯 Sobre o docker-compose.dev.yml

### ❓ Devo Manter ou Remover?

**✅ MANTER** - O arquivo `mlwrapper/docker-compose.dev.yml` é útil e deve ser mantido!

### 📋 Propósito

O `docker-compose.dev.yml` é um ambiente de desenvolvimento isolado para o **Flask ML Wrapper** que oferece:

1. **Hot Reload** - Alterações no código Python são refletidas automaticamente
2. **Debug Mode** - Logs detalhados e stack traces completos
3. **Isolamento** - Desenvolvimento independente sem afetar outros serviços
4. **Mock ML Integrado** - Não precisa do serviço ML real

### 🔄 Diferenças: dev vs produção

| Aspecto | docker-compose.dev.yml | docker-compose.yml (raiz) |
|---------|------------------------|---------------------------|
| **Localização** | `mlwrapper/` | Raiz do projeto |
| **Escopo** | Apenas Flask Wrapper | Sistema completo |
| **Hot Reload** | ✅ Sim (volumes) | ❌ Não |
| **Debug** | ✅ FLASK_DEBUG=True | ❌ FLASK_DEBUG=False |
| **Logs** | DEBUG | INFO |
| **ML Service** | Mock inline | Container separado |
| **Uso** | Desenvolvimento Python | Produção/Integração |

## 🚀 Como Usar

### Desenvolvimento do Flask Wrapper

Quando você está trabalhando **apenas** no código Python (Flask Wrapper):

```powershell
# Entrar na pasta do wrapper
cd d:\FlightOnTime\mlwrapper

# Subir ambiente de desenvolvimento
docker compose -f docker-compose.dev.yml up

# Ou em background
docker compose -f docker-compose.dev.yml up -d
```

**Vantagens:**
- ✅ Mudanças no código são aplicadas instantaneamente
- ✅ Não precisa rebuildar a imagem a cada alteração
- ✅ Logs mais detalhados para debug
- ✅ Mais rápido para testar mudanças

### Sistema Completo (Integração)

Quando você precisa testar **toda a aplicação integrada**:

```powershell
# Voltar para raiz
cd d:\FlightOnTime

# Subir sistema completo
docker compose --profile mock up -d
```

**Uso:**
- ✅ Testes de integração Java ↔ Python ↔ ML
- ✅ Testes end-to-end
- ✅ Simulação de ambiente produção
- ✅ Validação do fluxo completo

## 📁 Estrutura dos docker-compose

```
FlightOnTime/
├── docker-compose.yml              # Sistema completo (produção)
│   ├── fot-api (Java)
│   ├── ml-wrapper (Python)
│   └── ml-service-mock
│
└── mlwrapper/
    └── docker-compose.dev.yml      # Desenvolvimento Flask (dev)
        ├── ml-wrapper-dev
        └── ml-service-mock-dev
```

## 🔧 Configuração do docker-compose.dev.yml

### Serviço ml-wrapper-dev

```yaml
ml-wrapper-dev:
  build:
    context: .
    dockerfile: Dockerfile
  ports:
    - "5000:5000"
  environment:
    - FLASK_ENV=development      # Modo desenvolvimento
    - FLASK_DEBUG=True           # Debug ativo
    - LOG_LEVEL=DEBUG            # Logs verbosos
  volumes:
    - ./app:/app/app             # ⭐ Hot reload - código app/
    - ./tests:/app/tests         # ⭐ Hot reload - testes
  command: python run.py         # Servidor Flask nativo
```

**Volumes montados:**
- `./app` → Mudanças no código refletem instantaneamente
- `./tests` → Mudanças em testes também

### Serviço ml-service-mock-dev

```yaml
ml-service-mock:
  image: python:3.11-slim
  command: >
    sh -c "pip install flask && python -c \"...código inline...\""
```

**Características:**
- Mock ML embutido no comando
- Não precisa de arquivo separado
- Ideal para desenvolvimento rápido

## 🎨 Workflows de Desenvolvimento

### Workflow 1: Desenvolvimento Python Isolado

**Cenário:** Você está implementando uma nova feature no Flask Wrapper

```powershell
# 1. Abrir pasta do wrapper
cd mlwrapper

# 2. Subir ambiente dev
docker compose -f docker-compose.dev.yml up

# 3. Fazer alterações no código
# Editar app/routes/prediction_routes.py

# 4. Testar - o servidor recarrega automaticamente!
curl http://localhost:5000/health

# 5. Ver logs em tempo real
# Os logs aparecem no terminal automaticamente
```

### Workflow 2: Teste de Integração Completa

**Cenário:** Você precisa testar Java → Python → ML

```powershell
# 1. Parar ambiente dev (se estiver rodando)
cd mlwrapper
docker compose -f docker-compose.dev.yml down

# 2. Voltar para raiz e subir tudo
cd ..
docker compose --profile mock up -d

# 3. Testar endpoint Java
curl http://localhost:8080/api/v1/predict

# 4. Verificar logs de todos os serviços
docker logs fot-api
docker logs ml-wrapper
docker logs ml-service-mock
```

### Workflow 3: Desenvolvimento com Testes

**Cenário:** TDD - Test Driven Development

```powershell
# 1. Subir ambiente dev
cd mlwrapper
docker compose -f docker-compose.dev.yml up -d

# 2. Executar testes no container
docker compose -f docker-compose.dev.yml exec ml-wrapper-dev pytest -v

# 3. Ou executar testes localmente (se tiver Python instalado)
pytest -v

# 4. Fazer alterações e testes rodam novamente
```

## 🔍 Debug e Logs

### Logs Detalhados (Development)

```powershell
# Com docker-compose.dev.yml
docker compose -f docker-compose.dev.yml logs -f ml-wrapper-dev
```

**Output:**
```
DEBUG - Request received: {'flightNumber': 'AA1234', ...}
DEBUG - Validating with Pydantic...
DEBUG - Sending to ML service: http://ml-service-mock-dev:8000/predict
DEBUG - ML response: {'prediction': 1, 'probability': 0.91}
DEBUG - Mapping probability -> confidence
INFO - Returning result to Java API
```

### Logs Produção (docker-compose.yml)

```powershell
# Com docker-compose.yml
docker logs ml-wrapper
```

**Output:**
```
INFO - Request received from Java API: AA1234
INFO - Forwarding to external ML service...
INFO - Returning result to Java API: {'prediction': 1, 'confidence': 0.91}
```

## 🧪 Testes

### Executar Testes no Ambiente Dev

```powershell
cd mlwrapper

# Subir container dev
docker compose -f docker-compose.dev.yml up -d

# Rodar testes
docker compose -f docker-compose.dev.yml exec ml-wrapper-dev pytest -v

# Com coverage
docker compose -f docker-compose.dev.yml exec ml-wrapper-dev pytest --cov=app tests/
```

### Executar Testes no Docker Compose Principal

```powershell
cd d:\FlightOnTime

# Profile de testes
docker compose --profile test run --rm ml-wrapper-tests
```

## 🔄 Hot Reload em Ação

### Sem docker-compose.dev.yml (Produção)

```powershell
# 1. Alterar código
# 2. Parar container
docker compose down
# 3. Rebuildar imagem
docker compose build ml-wrapper
# 4. Subir novamente
docker compose up -d
```

**Tempo:** ~30-60 segundos por ciclo

### Com docker-compose.dev.yml (Development)

```powershell
# 1. Alterar código
# 2. Salvar arquivo
# Flask detecta mudança e recarrega automaticamente
```

**Tempo:** ~1-2 segundos

## 📊 Quando Usar Cada Um

### Use `docker-compose.dev.yml` quando:

- ✅ Desenvolvendo features no Flask Wrapper
- ✅ Debugando problemas no Python
- ✅ Fazendo mudanças frequentes no código
- ✅ Escrevendo/rodando testes Python
- ✅ Testando rotas Flask isoladamente
- ✅ Ajustando configurações do Wrapper

### Use `docker-compose.yml` quando:

- ✅ Testando integração completa
- ✅ Validando fluxo end-to-end
- ✅ Simulando ambiente de produção
- ✅ Testando comunicação entre containers
- ✅ Fazendo testes de carga
- ✅ Validando configurações de rede

## 🎯 Boas Práticas

### 1. Desenvolvimento Iterativo

```powershell
# Sempre começar com dev para mudanças rápidas
cd mlwrapper
docker compose -f docker-compose.dev.yml up -d

# Após validar, testar integração
cd ..
docker compose --profile mock up -d
```

### 2. Limpeza Regular

```powershell
# Limpar ambiente dev
cd mlwrapper
docker compose -f docker-compose.dev.yml down -v

# Limpar ambiente completo
cd ..
docker compose down -v
```

### 3. Alternância de Ambientes

```powershell
# Garantir que não há conflito de portas
# Parar um antes de subir outro

# Parar dev
cd mlwrapper
docker compose -f docker-compose.dev.yml down

# Subir produção
cd ..
docker compose --profile mock up -d
```

## 🚨 Problemas Comuns

### Porta 5000 em uso

**Problema:** Ambos os docker-compose tentam usar porta 5000

**Solução:**
```powershell
# Parar o que estiver rodando
docker compose -f docker-compose.dev.yml down
# OU
docker compose down

# Subir apenas um
```

### Hot Reload não funciona

**Problema:** Mudanças no código não são aplicadas

**Verificar:**
```powershell
# 1. Confirmar que volumes estão montados
docker compose -f docker-compose.dev.yml exec ml-wrapper-dev ls -la /app/app

# 2. Verificar se FLASK_DEBUG=True
docker compose -f docker-compose.dev.yml exec ml-wrapper-dev env | grep FLASK

# 3. Reiniciar container se necessário
docker compose -f docker-compose.dev.yml restart ml-wrapper-dev
```

## ✅ Resumo: Manter ou Remover?

### ✅ MANTER - Motivos:

1. **Produtividade** - Hot reload economiza muito tempo
2. **Debug** - Logs detalhados facilitam desenvolvimento
3. **Isolamento** - Trabalhar sem afetar outros serviços
4. **Padrão da indústria** - Ter ambientes dev/prod separados
5. **Testes rápidos** - Ciclo de desenvolvimento mais ágil

### ❌ Remover apenas se:

- Não for fazer mais mudanças no Flask Wrapper
- Projeto entrar em modo "somente manutenção"
- Quiser simplificar estrutura (não recomendado)

## 📝 Conclusão

O `docker-compose.dev.yml` é uma ferramenta valiosa para desenvolvimento ágil do Flask Wrapper. **Mantenha-o** e use conforme necessário para acelerar seu workflow de desenvolvimento!

---

**Última atualização:** 21 de dezembro de 2025
