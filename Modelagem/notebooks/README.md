# ✈️ Previsão de Atrasos de Voos Comerciais (ANAC)

Este projeto apresenta um pipeline completo de Ciência de Dados — **Coleta, Limpeza e Modelagem** — focado em prever atrasos de voos comerciais no Brasil. O sistema utiliza dados históricos da ANAC (Agência Nacional de Aviação Civil) para treinar um modelo de classificação binária.

## 📂 Estrutura do Repositório

O projeto está dividido em três etapas sequenciais, representadas pelos seguintes notebooks:

### 1. `scrap_voos.ipynb` (Coleta de Dados / Crawler)
Responsável pela ingestão de dados brutos diretamente da API da ANAC.
* **Resiliência:** Implementa um sistema de *checkpoint* (`checkpoint.txt`) para retomar downloads interrompidos e *retry* automático em caso de falhas de conexão.
* **Big Data:** Realiza o download mês a mês e escreve em disco (Google Drive) em modo *append* para evitar estouro de memória RAM (Streaming & Chunking).
* **Correção de Dados:** Trata erros de parsing JSON nativos da API da ANAC.

### 2. `Limpeza_dos_dados_ANAC.ipynb` (Pré-processamento)
Transforma os dados brutos em um dataset analítico pronto para ML.
* **Enriquecimento (ICAO -> IATA):** Mapeia códigos de aeroportos (ex: SBGR -> GRU) utilizando uma base auxiliar (`airports.csv`) para padronização comercial.
* **Definição do Target:** Cria a variável alvo binária:
    * `0`: Voos Pontuais ou Antecipados.
    * `1`: Voos com Atraso.
    * *(Voos cancelados são removidos para não enviesar o modelo)*.
* **Prevenção de Data Leakage:** Remove colunas que contêm a resposta do futuro, como `ds_situacao_voo` e `ds_situacao_chegada`.

### 3. `Treinamento_RF.ipynb` (Machine Learning)
Treinamento e validação do modelo preditivo.
* **Engenharia de Atributos:** Extração de sazonalidade através da classe `ExtratorDeDatas` (Mês, Dia da Semana, Hora, Dia do Ano).
* **Encoding:** Utiliza `TargetEncoder` para lidar com variáveis de alta cardinalidade (Aeroportos, N° de Voo, Empresas).
* **Balanceamento:** Aplica `RandomUnderSampler` nos dados de treino para equilibrar a classe majoritária (Pontuais) com a minoritária (Atrasos).
* **Modelo:** Random Forest Classifier otimizado com `class_weight='balanced'`.

---

## 🛠️ Tecnologias e Bibliotecas

* **Linguagem:** Python 3
* **Coleta:** `requests`, `urllib3`, `json`
* **Manipulação de Dados:** `pandas`, `numpy`
* **Machine Learning:** `scikit-learn`, `imblearn` (Imbalanced-learn), `joblib`
* **Ambiente:** Google Colab (integração com Google Drive)

---

## 📊 Performance do Modelo

O problema foi abordado como uma **Classificação Binária**. Dado o desbalanceamento natural dos voos, o foco do modelo foi maximizar o **Recall** (capacidade de detectar atrasos reais).

**Resultados no conjunto de teste:**

| Métrica | Valor Aprox. | Interpretação |
| :--- | :--- | :--- |
| **Acurácia** | ~70% | Taxa de acerto global do modelo. |
| **Recall (Classe 1)** | **~62%** | O modelo identifica corretamente 62% dos voos que realmente atrasaram. |
| **Precisão (Classe 1)** | ~18% | De todos os alertas de atraso gerados, 18% se confirmam (indica presença de Falsos Positivos). |

> **Nota:** O modelo demonstra robustez para identificar riscos baseados em sazonalidade e rotas, mas possui um teto de performance devido à ausência de variáveis dinâmicas em tempo real (ex: meteorologia).

---

## 🚀 Como Executar

Para reproduzir o projeto, siga a ordem de execução dos notebooks:

1.  **Coleta:** Execute `scrap_voos.ipynb`.
    * *Obs:* O script criará a estrutura de pastas no Google Drive (`/Dados_ANAC`).
2.  **Preparação:** Execute `Limpeza_dos_dados_ANAC.ipynb`.
    * *Requisito:* É necessário o arquivo auxiliar `airports.csv` para o mapeamento de aeroportos.
3.  **Treinamento:** Execute `Treinamento_RF.ipynb`.
    * Este notebook lerá os dados limpos, treinará o modelo e salvará o arquivo `.pkl` final na pasta `Modelos`.

---

## 📦 Exportação

O pipeline final é exportado utilizando `joblib` no arquivo `modelo_atraso_voos_rf_res.pkl`. Ele encapsula todo o pré-processamento e o modelo treinado, garantindo que novos dados passem pelas mesmas transformações matemáticas.
