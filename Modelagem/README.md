# 🧪 Data Science & Modelagem

Este diretório concentra o fluxo de trabalho de ciência de dados, desde a análise exploratória até o treinamento de modelos preditivos, utilizando a base de dados de voos da ANAC.

## 🎯 Objetivos da Equipe

- **Pré-processamento:** Limpeza e feature engineering dos dados brutos coletados pelo scraper.
- **EDA (Análise Exploratória):** Identificação de padrões de atrasos, sazonalidade e eficiência das companhias aéreas.
- **Modelagem:** Desenvolvimento e validação de algoritmos de Machine Learning.

## 📂 Estrutura

- **`/notebooks`:** Ambientes de experimentação e prototipagem Jupyter.
  - Notebooks para limpeza de dados, análise exploratória e treinamento de modelos.
- **`/Modelos`:** Binários dos modelos treinados e serializados (.pkl, .bin, .joblib) e aplicação de serviço.
  - Inclui Dockerfile e scripts para servir o modelo via API REST.

## 🚀 Como Usar

### Pré-requisitos

- Python 3.11+
- Jupyter Notebook ou JupyterLab
- Docker (para servir o modelo)

### Executando os Notebooks

```bash
cd Modelagem/notebooks
pip install -r requirements.txt  # se houver
jupyter notebook
```

### Servindo o Modelo

Consulte [Modelos/README.md](Modelos/README.md) para instruções detalhadas sobre como servir o modelo treinado.

## 📊 Dados

Os dados são provenientes da ANAC (Agência Nacional de Aviação Civil) e incluem informações sobre voos domésticos no Brasil.

## 🤝 Contribuindo

Para contribuir com novos modelos ou análises, consulte [CONTRIBUTING.md](../docs/CONTRIBUTING.md)