#!/bin/bash
# Script para baixar o modelo ML de uma GitHub Release
# Uso: ./download-model.sh [release-tag] [output-dir]

set -e

RELEASE_TAG="${1:-v1.0.0}"
OUTPUT_DIR="${2:-Modelagem/Modelos}"
MODEL_FILE="modelo_atraso_voos_rf_res.pkl"
REPO="Mateus-Redivo/FlightOnTime"

echo "📦 Baixando modelo ML da release ${RELEASE_TAG}..."
echo "📁 Destino: ${OUTPUT_DIR}/${MODEL_FILE}"

# Cria o diretório se não existir
mkdir -p "${OUTPUT_DIR}"

# URL do asset na release
RELEASE_URL="https://github.com/${REPO}/releases/download/${RELEASE_TAG}/${MODEL_FILE}"

# Baixa o arquivo usando curl com retry
curl -L \
  --retry 3 \
  --retry-delay 5 \
  --max-time 600 \
  -H "Accept: application/octet-stream" \
  -o "${OUTPUT_DIR}/${MODEL_FILE}" \
  "${RELEASE_URL}"

# Verifica se o download foi bem-sucedido
if [ -f "${OUTPUT_DIR}/${MODEL_FILE}" ]; then
  FILE_SIZE=$(du -h "${OUTPUT_DIR}/${MODEL_FILE}" | cut -f1)
  echo "✅ Modelo baixado com sucesso! Tamanho: ${FILE_SIZE}"
else
  echo "❌ Erro ao baixar o modelo"
  exit 1
fi
