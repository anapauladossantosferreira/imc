// script.js - JavaScript da Calculadora de IMC

// Função principal chamada ao clicar no botão
function calcularIMC() {
    // Pega os valores dos campos
    const peso = parseFloat(document.getElementById('peso').value);
    const altura = parseFloat(document.getElementById('altura').value);
    const resultadoDiv = document.getElementById('resultado');
    
    // Validação dos campos
    if (!peso || !altura || peso <= 0 || altura <= 0) {
        resultadoDiv.innerHTML = `<p style="color: red;">❌ Por favor, preencha peso e altura corretamente.</p>`;
        resultadoDiv.style.display = 'block';
        return;
    }

    // Calcula o IMC
    const imc = peso / (altura * altura);
    
    let classificacao = '';
    let emoji = '';

    // Define classificação e emoji
    if (imc < 18.5)      { classificacao = "Abaixo do peso"; emoji = "📉"; }
    else if (imc < 25)   { classificacao = "Peso normal"; emoji = "✅"; }
    else if (imc < 30)   { classificacao = "Sobrepeso"; emoji = "⚠️"; }
    else if (imc < 35)   { classificacao = "Obesidade grau 1"; emoji = "🚨"; }
    else if (imc < 40)   { classificacao = "Obesidade grau 2"; emoji = "🚨"; }
    else                 { classificacao = "Obesidade grau 3"; emoji = "🚨"; }

    // Exibe o resultado
    resultadoDiv.innerHTML = `
        <h2>Seu Resultado</h2>
        <p class="imc-value">IMC: <strong>${imc.toFixed(2)}</strong></p>
        <p>${emoji} ${classificacao}</p>
        <p>Peso: ${peso} kg | Altura: ${altura} m</p>
    `;
    resultadoDiv.style.display = 'block';

    // Salva no histórico
    salvarNoHistorico(peso, altura, imc, classificacao);
}

// Atualiza o preview em tempo real enquanto digita
function atualizarPreview() {
    const peso = parseFloat(document.getElementById('peso').value);
    const altura = parseFloat(document.getElementById('altura').value);
    const previewDiv = document.getElementById('preview');

    if (peso && altura && peso > 0 && altura > 0) {
        const imc = peso / (altura * altura);
        let emoji = imc < 18.5 ? "📉" : imc < 25 ? "✅" : imc < 30 ? "⚠️" : "🚨";
        
        previewDiv.innerHTML = `<strong>Preview:</strong> IMC ≈ ${imc.toFixed(2)} ${emoji}`;
        previewDiv.style.display = 'block';
    } else {
        previewDiv.style.display = 'none';
    }
}

// Salva cálculo no localStorage
function salvarNoHistorico(peso, altura, imc, classificacao) {
    let historico = JSON.parse(localStorage.getItem('historicoIMC') || '[]');
    
    historico.unshift({
        data: new Date().toLocaleString('pt-BR'),
        peso: peso,
        altura: altura,
        imc: imc.toFixed(2),
        classificacao: classificacao
    });

    if (historico.length > 10) historico.pop(); // Mantém apenas 10 registros
    
    localStorage.setItem('historicoIMC', JSON.stringify(historico));
    carregarHistorico();
}

// Carrega o histórico na tela
function carregarHistorico() {
    const lista = document.getElementById('lista-historico');
    const historico = JSON.parse(localStorage.getItem('historicoIMC') || '[]');
    
    lista.innerHTML = '';
    historico.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.data} — IMC: ${item.imc} | ${item.classificacao}`;
        lista.appendChild(li);
    });
}

// Adiciona eventos de digitação
document.getElementById('peso').addEventListener('input', atualizarPreview);
document.getElementById('altura').addEventListener('input', atualizarPreview);

// Carrega histórico quando a página abre
window.onload = carregarHistorico;