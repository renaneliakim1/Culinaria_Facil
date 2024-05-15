
    function limparCampos() {
        // Limpa o campo de imagem da receita
        document.getElementById("form-imagem_receita").value = "";
        document.getElementById("file-name-imagem").textContent = "Nenhum arquivo selecionado";

        // Limpa o campo de vídeo da receita
        document.getElementById("form-video_receita").value = "";
        document.getElementById("file-name-video").textContent = "Nenhum arquivo selecionado";

        // Limpa o campo do nome da receita
        document.getElementById("form-titulo_receita").value = "";

        // Limpa o campo da descrição da receita
        document.getElementById("form-descricao_receita").value = "";

        // Limpa o campo de ingredientes da receita
        document.getElementById("form-ingredientes_receita").value = "";

        // Limpa o campo de instruções da receita
        document.getElementById("form-instrucoes_receita").value = "";

        // Limpa o campo de tempo de preparo
        document.getElementById("tempo_preparo").value = "";

        // Desmarca todos os botões de rádio de dificuldade
        var radios = document.getElementsByName("dificuldade_receita");
        for (var i = 0; i < radios.length; i++) {
            radios[i].checked = false;
        }

        // Desmarca a opção de categoria
        document.getElementById("form-categoria_receita").selectedIndex = -1;
    }
