document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('ingredientes_receita');
    
    textarea.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Evita que a quebra de linha padrão ocorra
            const cursorPosition = textarea.selectionStart;
            const textBeforeCursor = textarea.value.substring(0, cursorPosition);
            const textAfterCursor = textarea.value.substring(cursorPosition);
            textarea.value = textBeforeCursor + '&#13;&#10;' + textAfterCursor; // Adiciona '&#13;&#10;' na posição do cursor
            textarea.selectionStart = cursorPosition + 10; // Move o cursor dez posições para frente
            textarea.selectionEnd = cursorPosition + 10;
        } else if (event.key === 'Backspace') {
            const cursorPosition = textarea.selectionStart;
            const textBeforeCursor = textarea.value.substring(0, cursorPosition);
            const textAfterCursor = textarea.value.substring(cursorPosition);
            if (textBeforeCursor.endsWith('&#13;&#10;')) {
                event.preventDefault(); // Evita o comportamento padrão do backspace
                textarea.value = textBeforeCursor.slice(0, -10) + textAfterCursor; // Remove o '&#13;&#10;' antes do cursor
                textarea.selectionStart = cursorPosition - 10; // Move o cursor dez posições para trás
                textarea.selectionEnd = cursorPosition - 10;
            }
        }
    });
});


