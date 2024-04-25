function outputUpdate(tempo_preparo) {
    var tempo_inteiro = Math.round(tempo_preparo);
    document.querySelector('#tempo_selecionado').textContent = tempo_inteiro + ' minutos';
}