
document.getElementById("flexSwitchCheckDefault").addEventListener("click", function () {
    document.body.classList.toggle("modo-escuro");
    // Adiciona ou remove a classe 'svg-branco' dependendo se o modo escuro está ativado ou não
    const svgs = document.querySelectorAll("svg");
    svgs.forEach(svg => {
        svg.classList.toggle("svg-branco", document.body.classList.contains("modo-escuro"));
    });
});



window.onscroll = function () { scrollFunction() };



/*   // modo escuro
       
       document
            .getElementById("flexSwitchCheckDefault")
            .addEventListener("click", function () {
                document.body.classList.toggle("modo-escuro");
            }); */