
function limparCampos() {
    // Limpa o campo de texto nome
    document.getElementById('nome').value = '';

    // Limpa o campo de texto ingredientes
    document.getElementById('ingredientes').value = '';

    // Limpa o campo de texto instrucoes
    document.getElementById('instrucoes').value = '';

    // Reseta o valor do tempo de cozimento (customRange1) para o valor padrão (8)
    document.getElementById('customRange1').value = 8;
    document.getElementById('valor').textContent = '8'; // Atualiza o texto exibido

    // Desmarca todos os checkboxes de categoria
    var checkboxes = document.querySelectorAll('#filtro input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = false;
    });

    // Desmarca todos os radios de dificuldade
    var radios = document.querySelectorAll('.radio-inputs input[type="radio"]');
    radios.forEach(function(radio) {
        radio.checked = false;
    });
}

// Chamada da função para limpar os campos quando necessário
limparCampos();
