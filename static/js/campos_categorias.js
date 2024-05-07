document.addEventListener("DOMContentLoaded", function() {
    var radios = document.querySelectorAll('input[type="radio"]');

    radios.forEach(function(radio) {
        radio.addEventListener('click', function(event) {
            var clickedRadio = event.target;
            var lastClicked = clickedRadio.dataset.lastClicked;
            var clickCount = parseInt(clickedRadio.dataset.clickCount) || 0;

            if (lastClicked === clickedRadio.id) {
                clickCount++;
            } else {
                lastClicked = clickedRadio.id;
                clickCount = 1;
            }

            if (clickCount >= 2) {
                var inputDefault = document.getElementById("categoria_receita-7");
                inputDefault.checked = true;
                clickCount = 0; // Resetar o contador após marcar a opção padrão
            }

            clickedRadio.dataset.clickCount = clickCount;
            clickedRadio.dataset.lastClicked = lastClicked;
        });
    });
});
