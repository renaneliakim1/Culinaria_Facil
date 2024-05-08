// Seleciona o elemento que contém o texto
var ingredientesElement = document.querySelector('.ingredientes li');

// Obtém o texto dentro da <li>
var texto = ingredientesElement.textContent;

// Remove as linhas vazias e depois divide o texto em linhas
var linhas = texto.split('\n').filter(function(linha) {
    return linha.trim() !== ''; // Remove as linhas que contêm apenas espaços em branco
});

// Limpa o conteúdo da <li>
ingredientesElement.textContent = '';

// Seleciona o elemento pai da <li>
var listaElement = ingredientesElement.parentNode;

// Para cada linha não vazia, cria um novo item de lista e adiciona à lista
linhas.forEach(function(linha) {
    var itemLista = document.createElement('li');
    itemLista.textContent = linha;
    listaElement.appendChild(itemLista);
});

// Seleciona o elemento que contém o texto
var preparoElement = document.querySelector('.preparo li');

// Obtém o texto dentro da <li>
var texto = preparoElement.textContent;

// Remove as linhas vazias e depois divide o texto em linhas
var linhas = texto.split('\n').filter(function(linha) {
    return linha.trim() !== ''; // Remove as linhas que contêm apenas espaços em branco
});

// Limpa o conteúdo da <li>
preparoElement.textContent = '';

// Seleciona o elemento pai da <li>
var listaElement = preparoElement.parentNode;

// Para cada linha não vazia, cria um novo item de lista e adiciona à lista
linhas.forEach(function(linha) {
    var itemLista = document.createElement('li');
    itemLista.textContent = linha;
    listaElement.appendChild(itemLista);
});
