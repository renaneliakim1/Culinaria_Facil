from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para o processamento do formulário
@app.route('/cadastrar_receita', methods=['POST'])
def cadastrar_receita():
    # Obtendo os dados do formulário
    nome = request.form['nome']
    ingredientes = request.form['ingredientes']
    instrucoes = request.form['instrucoes']
    
    # Aqui você pode processar os dados como desejar
    # Por exemplo, salvar em um banco de dados, enviar por e-mail, etc.
    
    # Retorna uma resposta em JSON
    return jsonify({'status': 'success', 'message': 'Receita cadastrada com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
