# FlyPredict | FYI - For Your Information ✈️

## 📑 Índice

* [Estrutura do Projeto](#-estrutura-do-projeto)
* [Funcionamento das Telas](#-funcionamento-das-telas)
* [Lógica do Script.js](#-lógica-do-scriptjs)
* [Tecnologias Utilizadas](#-tecnologias-utilizadas)

---

## 📂 Estrutura do Projeto

* `index.html`: Portal principal de interação e consulta.
* `ajuda.html`: Central unificada de documentação técnica e suporte.
* `style.css`: Motor visual com variáveis de cores, layouts flexíveis e animações.
* `script.js`: Lógica de processamento, animações de entrada e simulação do modelo preditivo.

---

## 🖥️ Funcionamento das Telas

### 1. Tela de Consulta (`index.html`)

É o "coração" do projeto.

* **O Formulário:** O usuário insere dados como companhia aérea, aeroporto e horário.
* **O Gauge (Velocímetro):** Após o processamento, um medidor circular dinâmico exibe a probabilidade de atraso.
* **Feedback Visual:** As cores mudam conforme o risco (Verde para baixo risco, Laranja para atenção e Vermelho para alto risco).
* **Experiência:** Utiliza animações de *reveal* para que os resultados apareçam suavemente na tela.

### 2. Central de Ajuda (`ajuda.html`)

Esta tela substituiu as antigas páginas de estatística e modelo, servindo como uma **Base de Conhecimento**:

* **Estatística:** Explica como padrões de sazonalidade e tendências influenciam o setor aéreo.
* **Machine Learning:** Detalha o processo de **ETL** (Extração, Transformação e Carga) e o treinamento do algoritmo *Random Forest*.
* **Contato:** Seção dedicada para suporte técnico e feedback com a equipe de desenvolvimento.
* **Navegação:** Design focado em leitura, com botões estratégicos para retornar à tela de consulta.

---

## 📜 Lógica do `script.js`

O arquivo de script gerencia o ciclo de vida da aplicação no navegador através de três pilares:

1. **Gestão de Estado do Formulário:** Intercepta o envio para simular o processamento, alterando labels de botões e estados de "disabled" para evitar erros de submissão duplicada.
2. **Cálculo do Gauge:** Transforma valores numéricos em rotações de estilo CSS (unidade `turn`). Um valor de 50% de probabilidade, por exemplo, aciona uma rotação de `0.25turn` no preenchimento do medidor.
3. **Sistema de Revelação (Reveal):** Monitora o carregamento do DOM para aplicar classes de animação de forma escalonada, garantindo que o conteúdo surja suavemente conforme a hierarquia de importância.

---

## ⚙️ Tecnologias Utilizadas

* **HTML5/CSS3:** Estrutura semântica e layout moderno com `Flexbox` e `CSS Grid`.
* **JavaScript (ES6+):** Manipulação de DOM e lógica de animações.
* **Font Awesome:** Biblioteca de ícones vetoriais.
* **Animações Customizadas:** Sistema de classes `.reveal` com delays em cascata para uma UI fluida.

---