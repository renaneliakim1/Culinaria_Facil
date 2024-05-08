
var ingredientesElement = document.querySelector('.ingredientes li');


var texto = ingredientesElement.textContent;
var linhas = texto.split('\n').filter(function(linha) {
    return linha.trim() !== ''; 
});


ingredientesElement.textContent = '';


var listaElement = ingredientesElement.parentNode;


linhas.forEach(function(linha) {
    var itemLista = document.createElement('li');
    itemLista.textContent = linha;
    listaElement.appendChild(itemLista);
});


var preparoElement = document.querySelector('.preparo li');


var texto = preparoElement.textContent;


var linhas = texto.split('\n').filter(function(linha) {
    return linha.trim() !== ''; 
});


preparoElement.textContent = '';


var listaElement = preparoElement.parentNode;


linhas.forEach(function(linha) {
    var itemLista = document.createElement('li');
    itemLista.textContent = linha;
    listaElement.appendChild(itemLista);
});
