#!/bin/bash
# Script auxiliar para Dockerfile: baixa o modelo apenas se não existir localmente
# Útil para builds locais e CI/CD

MODEL_FILE="modelo_atraso_voos_rf_res.pkl"
RELEASE_TAG="${MODEL_RELEASE_TAG:-v1.0.0}"
REPO="${GITHUB_REPOSITORY:-Mateus-Redivo/FlightOnTime}"

if [ -f "${MODEL_FILE}" ]; then
  echo "✅ Modelo já existe localmente: ${MODEL_FILE}"
  exit 0
fi

echo "⬇️ Modelo não encontrado, baixando da release ${RELEASE_TAG}..."

RELEASE_URL="https://github.com/${REPO}/releases/download/${RELEASE_TAG}/${MODEL_FILE}"

curl -L \
  --retry 3 \
  --retry-delay 5 \
  --max-time 600 \
  -o "${MODEL_FILE}" \
  "${RELEASE_URL}" || {
    echo "❌ Falha ao baixar modelo. Verifique se a release ${RELEASE_TAG} existe."
    exit 1
  }

echo "✅ Modelo baixado com sucesso!"
