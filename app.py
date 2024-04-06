from flask import Flask, render_template, request
import requests

app = Flask(__name__)

class ReceitasCulinarias:
    def __init__(self):
        self.url_base = "https://www.themealdb.com/api/json/v1/1/"
    
    def obter_receitas_por_regiao(self, regiao):
        url = f"{self.url_base}filter.php?a={regiao}"
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            return dados['meals']
        else:
            return None

receitas = ReceitasCulinarias()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    regiao = request.form['regiao']
    receitas_regiao = receitas.obter_receitas_por_regiao(regiao)
    return render_template('resultado.html', regiao=regiao, receitas=receitas_regiao)

if __name__ == '__main__':
    app.run(debug=True)