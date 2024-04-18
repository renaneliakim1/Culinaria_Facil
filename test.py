from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Conectar ao banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="nome_do_banco_de_dados"
)

# Criar um cursor para executar comandos SQL
cur = conn.cursor()

# Rota para a página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Rota para lidar com a busca de receitas
@app.route("/buscar_receitas", methods=["POST"])
def buscar_receitas():
    categoria = request.form["categoria"]
    cur.execute("SELECT * FROM receitas WHERE categoria=%s", (categoria,))
    receitas = cur.fetchall()
    return render_template("resultado.html", receitas=receitas)

# Rota para lidar com a página de erro 404
@app.errorhandler(404)
def not_found(error):
    return "Página não encontrada", 404





# Inicializar o servidor
if __name__ == "__main__":
    app.run(debug=True)
