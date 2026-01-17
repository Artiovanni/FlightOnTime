/**
 * Lógica Principal do Formulário de Predição
 */
// Detecta se está rodando em desenvolvimento (Live Server) ou produção (Docker/nginx)
const isDevelopment = window.location.port === '5500' || window.location.port === '5501';
const isDocker = window.location.port === '3000' || window.location.port === '' || window.location.port === '80';
const API_URL = isDevelopment 
    ? 'http://localhost:8080/api/v1/predict'  // Live Server - aponta direto para backend
    : '/api/v1/predict';  // Docker/nginx (porta 3000) - usa proxy

console.log('Porta detectada:', window.location.port);
console.log('Ambiente:', isDevelopment ? 'Live Server' : (isDocker ? 'Docker' : 'Produção'));
console.log('API URL:', API_URL);

const predictForm = document.getElementById('predict-form');
// Verificamos se o formulário existe na página atual antes de adicionar o listener
if (predictForm) {
    predictForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const btn = e.target.querySelector('button');
        const resultCard = document.getElementById('result-card');
        
        // Elementos do Gauge (Velocímetro)
        const gaugeFill = document.getElementById('gauge-fill');
        const gaugeText = document.getElementById('gauge-text');
        const statusTitle = document.getElementById('result-status');
        const statusDesc = document.getElementById('result-description');

        // 1. Estado de Carregamento
        btn.innerText = "Calculando Probabilidade...";
        btn.disabled = true;

        try {
            // Coletar dados do formulário
            const formData = new FormData(e.target);
            const flightDate = formData.get('flightDate');
            const flightTime = formData.get('flightTime');
            
            // Combinar data e hora no formato ISO
            const flightDepartureDate = `${flightDate}T${flightTime}:00`;
            
            const requestData = {
                flightNumber: formData.get('flightNumber'),
                companyName: formData.get('companyName'),
                flightOrigin: formData.get('flightOrigin'),
                flightDestination: formData.get('flightDestination'),
                flightDepartureDate: flightDepartureDate,
                flightDistance: Number.parseInt(formData.get('flightDistance'))
            };

            // Chamar a API
            console.log('Enviando requisição para:', API_URL);
            console.log('Dados:', requestData);
            
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Erro da API:', errorText);
                throw new Error(`Erro na API: ${response.status} - ${errorText}`);
            }

            const data = await response.json();
            console.log('Resposta da API:', data);
            
            // Restaurar botão
            btn.innerText = "Analisar Probabilidade";
            btn.disabled = false;
            
            // Usar probabilidade da API
            const probabilidade = Math.round(data.probabilityPercentage);
            
            // 2. Exibir o Card de Resultado
            resultCard.style.display = "block";
            
            // Pequeno delay para garantir que o display:block foi processado antes do scroll
            setTimeout(() => {
                resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);

            // 3. Animar o Gauge (0.5 turn equivale a 100% no CSS semi-circular)
            const turnValue = (probabilidade / 100) * 0.5;
            gaugeFill.style.transform = `rotate(${turnValue}turn)`;
            gaugeText.innerText = `${probabilidade}%`;

            // 4. Lógica de Cores e Feedback Visual baseado na predição
            if (data.prediction === "ON_TIME") {
                gaugeFill.style.background = "#4caf50"; // Verde
                statusTitle.innerText = "Voo Pontual";
                statusTitle.className = "status-low";
                statusDesc.innerText = `${data.summary} - As condições históricas sugerem que este voo tem altíssima chance de decolar no horário previsto.`;
            } else {
                // DELAYED
                if (probabilidade <= 60) {
                    gaugeFill.style.background = "#ff9800"; // Laranja
                    statusTitle.innerText = "Atenção Necessária";
                    statusTitle.className = "status-medium";
                    statusDesc.innerText = `${data.summary} - Existe uma probabilidade moderada de pequenos atrasos. Recomendamos acompanhar o painel do aeroporto.`;
                } else {
                    gaugeFill.style.background = "#f44336"; // Vermelho
                    statusTitle.innerText = "Risco de Atraso";
                    statusTitle.className = "status-high";
                    statusDesc.innerText = `${data.summary} - Probabilidade elevada de atraso detectada. Fatores como congestionamento aéreo ou histórico da rota influenciam este resultado.`;
                }
            }

        } catch (error) {
            let errorMessage = 'Erro ao processar a predição. ';
            
            if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                errorMessage += '\n\nVerifique se:\n- O backend está rodando em http://localhost:8080\n- Execute: docker compose up fot-api';
            } else if (error.message.includes('405')) {
                errorMessage += '\n\nMétodo POST não permitido. Verifique a configuração CORS do backend.';
            } else {
                errorMessage += '\n\n' + error.message;
            }
            
            alert(errorMessage);
            console.error('Erro ao fazer a predição:', error);
            
            // Restaurar botão
            btn.innerText = "Analisar Probabilidade";
            btn.disabled = false;
        }
    });
}

/**
 * Lógica de Animação de Entrada (Reveal)
 * Ativa as classes .reveal presentes no HTML ao carregar a página
 */
window.addEventListener('load', () => {
    const scrollElements = document.querySelectorAll('.reveal');
    
    // Adiciona a classe active com um pequeno delay para garantir fluidez
    setTimeout(() => {
        scrollElements.forEach((el) => {
            el.classList.add('active');
        });
    }, 100);
});