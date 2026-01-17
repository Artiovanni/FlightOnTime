# Usamos Python 3.11 Slim para garantir compatibilidade com scikit-learn 1.6+ e numpy 2.0+
# (Imagens alpine podem ter problemas de compilação com numpy/pandas novos)
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# 1. Copia apenas o requirements primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# 2. Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia o app.py
COPY app.py ./

# 4. Baixa o modelo da release se não existir no build context
RUN echo "📥 Verificando modelo ML..."; \
    if [ ! -f modelo_atraso_voos_rf_res.pkl ]; then \
      echo "⬇️ Baixando modelo da release v1.0.0 (~667 MB, pode demorar alguns minutos)..."; \
      apt-get update -qq && apt-get install -y -qq curl && \
      curl -L --progress-bar -o modelo_atraso_voos_rf_res.pkl \
        https://github.com/Mateus-Redivo/FlightOnTime/releases/download/v1.0.0/modelo_atraso_voos_rf_res.pkl || \
        (echo "❌ Falha ao baixar modelo. Verifique se a release v1.0.0 existe." && exit 1); \
      echo "✅ Modelo baixado com sucesso!"; \
    else \
      echo "✅ Modelo já existe no build context"; \
    fi

# 4b. Se o modelo existir localmente, copia (opcional, para otimizar rebuilds)
# Descomente a linha abaixo se você tiver o modelo local e quiser usar cache
# COPY modelo_atraso_voos_rf_res.pkl* ./ 2>/dev/null || true

# Expõe a porta 5000 (padrão definido no seu app.py)
EXPOSE 5000

# Comando para iniciar a aplicação
# Nota: Para produção real, recomenda-se usar gunicorn, mas python app.py funciona para este setup
CMD ["python", "app.py"]
