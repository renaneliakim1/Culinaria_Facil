/* 
document.getElementById("flexSwitchCheckDefault").addEventListener("click", function () {
    document.body.classList.toggle("modo-escuro");
    // Adiciona ou remove a classe 'svg-branco' dependendo se o modo escuro está ativado ou não
    const svgs = document.querySelectorAll("svg");
    svgs.forEach(svg => {
        svg.classList.toggle("svg-branco", document.body.classList.contains("modo-escuro"));
    });
});
 */

window.onscroll = function () { scrollFunction() };
 
/*   // modo escuro
       
       document
            .getElementById("flexSwitchCheckDefault")
            .addEventListener("click", function () {
                document.body.classList.toggle("modo-escuro");
            }); */




/* ----------------------------------------------------------------------------------- */

// Função para definir o modo escuro
function enableDarkMode() {
    document.body.classList.add('modo-escuro');
    localStorage.setItem('modo', 'escuro');
}

// Função para definir o modo claro
function enableLightMode() {
    document.body.classList.remove('modo-escuro');
    localStorage.setItem('modo', 'claro');
}

// Verificar a preferência do usuário ao carregar a página
window.onload = function() {
    const modoSalvo = localStorage.getItem('modo');

    if (modoSalvo === 'escuro') {
        enableDarkMode();
    } else {
        enableLightMode();
    }
};

// Adicionar um evento de clique para alternar entre os modos
document.getElementById('flexSwitchCheckDefault').addEventListener('click', function() {
    if (document.body.classList.contains('modo-escuro')) {
        enableLightMode();
    } else {
        enableDarkMode();
    }
});


// Função para definir o modo escuro
function enableDarkMode() {
    document.body.classList.add('modo-escuro');
    localStorage.setItem('modo', 'escuro');
    // Altera a cor dos SVGs para branco
    const svgs = document.querySelectorAll("svg");
    svgs.forEach(svg => {
        svg.classList.add("svg-branco");
    });
}

// Função para definir o modo claro
function enableLightMode() {
    document.body.classList.remove('modo-escuro');
    localStorage.setItem('modo', 'claro');
    // Altera a cor dos SVGs de volta para a cor original
    const svgs = document.querySelectorAll("svg");
    svgs.forEach(svg => {
        svg.classList.remove("svg-branco");
    });
}




