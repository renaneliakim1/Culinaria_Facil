from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from forms import FormularioRegistro, FormularioLogin, FormularioReceita
import mysql.connector
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import email_validator


try:
    database_connection = mysql.connector.connect(user='root', password='', host='localhost', database='sitereceita')
    print('Conexão com banco de dados bem sucedida')
except:
    print('Erro ao conectar ao banco de dados')


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = '34#%#$tFDBXCBGHThfd4¨%$28*(86'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']



@app.route('/')
def pagina_inicial():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    else:
        return render_template('index.html')


@app.route('/receitas/<int:pagina>')
def pagina_receitas(pagina):
    cursor = database_connection.cursor()
    consulta_receitas = 'SELECT * FROM receitas'
    cursor.execute(consulta_receitas)
    resultado = cursor.fetchall()
    inicio_pagina = (pagina-1)*10
    fim_pagina = pagina*10
    resultado_receita= resultado[inicio_pagina:fim_pagina]
    if len(resultado_receita) >0:
        return render_template('receitas.html', resultado_receita=resultado_receita, pagina=pagina)
    else:
        return redirect(url_for('pagina_inicial'))


@app.route('/receita/<int:receita_id>')
def pagina_receita(receita_id):
    cursor = database_connection.cursor()
    consulta_receita = 'SELECT receitaID, Titulo, descricao, Instrucoes, ingredientes, tempoPreparo, Dificuldade, usuario.nome, usuario.id, data_hora FROM receitas inner join usuario  on receitas.autorID = usuario.id WHERE receitaID = %s'
    cursor.execute(consulta_receita, (receita_id,))
    resultado_receita = cursor.fetchall()
    return render_template('receita.html', resultado_receita=resultado_receita)


@app.route('/minhas_receitas/<int:pagina>')
def minhas_receita(pagina):
    if 'user' in session:
        cursor = database_connection.cursor()
        consulta_receita = 'SELECT * FROM receitas WHERE AutorID = %s'
        autor_id = session['user'][0]
        cursor.execute(consulta_receita, (autor_id,))
        resultado = cursor.fetchall()
        inicio_pagina = (pagina-1)*10
        fim_pagina = pagina*10
        resultado_receita= resultado[inicio_pagina:fim_pagina]
        if len(resultado_receita) >0:
            return render_template('usuario_receitas.html', resultado_receita=resultado_receita)
        else:
            flash("Você não possui receitas cadastradas.")
            return redirect(url_for('cadastro_receita'))
    else:
        return redirect(url_for('pagina_inicial'))


@app.route('/cadastro', methods=['POST', 'GET'])
def pagina_registro():
    if 'user' in session:
        return redirect(url_for('pagina_inicial'))
    else:
        form = FormularioRegistro()
        if form.validate_on_submit():
            registro_nome = form.registro_nome.data
            registro_email = form.registro_email.data
            registro_cpf = form.registro_cpf.data
            registro_senha = form.registro_senha.data
            cursor = database_connection.cursor()
            consulta_email = 'SELECT email FROM usuario WHERE email = %s'
            cursor.execute(consulta_email, (registro_email,))
            resultado = cursor.fetchone()
            cursor.close()
            if resultado:
                flash('Conta já Existe. Faça Login')
                return redirect(url_for('pagina_registro'))
            else:
                if registro_cpf.isnumeric():
                    senha_hasheada = bcrypt.generate_password_hash(registro_senha).decode('utf-8')
                    inserir_dados = 'INSERT INTO usuario(nome, email, cpf, senha) VALUES (%s, %s, %s, %s)'
                    dados_usuario = (registro_nome, registro_email, registro_cpf, senha_hasheada)
                    cursor = database_connection.cursor()
                    cursor.execute(inserir_dados, dados_usuario)
                    database_connection.commit()
                    cursor.close()
                    flash('Conta Criada com Sucesso. Faça Login')
                    return redirect(url_for('pagina_login'))
                else:
                    flash('Digite apenas números no CPF')
                    return redirect(url_for('pagina_registro'))
    return render_template('registerpage.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def pagina_login():
    if 'user' in session:
        return redirect(url_for('pagina_inicial'))
    else:
        form = FormularioLogin()
        if form.validate_on_submit():
            login_email = form.login_email.data
            login_senha = form.login_senha.data
            cursor = database_connection.cursor()
            consulta_conta = 'SELECT id, nome,email, senha FROM usuario WHERE email = %s'
            cursor.execute(consulta_conta, (login_email,))
            resultado = cursor.fetchall()
            cursor.close()
            if resultado:
                id_verificado, nome_verificado, email_verificado, senha_verificada = resultado[0]
                verificar_senha = bcrypt.check_password_hash(senha_verificada, login_senha)
                if verificar_senha:
                    session['user'] = resultado[0]
                    return redirect(url_for('pagina_inicial'))
                else:
                    flash('Email ou senha incorretos')
                    return redirect(url_for('pagina_login'))
            else:
                flash('Email ou senha incorretos')
                return redirect(url_for('pagina_login'))
    return render_template('loginpage.html', form=form)


@app.route('/perfil/<int:id_usuario>')
def pagina_perfil(id_usuario):
    cursor = database_connection.cursor()
    consulta_usuario = 'SELECT usuario.id,usuario.nome, usuario.email FROM usuario WHERE  usuario.id= %s'
    cursor.execute(consulta_usuario, (id_usuario,))
    resultado = cursor.fetchall()
    cursor.close()
    if resultado:
        cursor = database_connection.cursor()
        consulta_receita_usuario = 'SELECT receitaID ,Titulo, Descricao, Instrucoes, ingredientes, TempoPreparo, Dificuldade, data_hora FROM usuario INNER JOIN receitas ON usuario.id = receitas.AutorID WHERE  usuario.id= %s ORDER BY data_hora DESC LIMIT 3'
        cursor.execute(consulta_receita_usuario, (id_usuario,))
        resultado_receitas = cursor.fetchall()
        cursor.close()
        if 'user' in session:
            if session['user'][0] == resultado[0][0]:
                return render_template('editar_perfil.html', resultado=resultado)
            else:
                return render_template('perfil.html', resultado=resultado, resultado_receitas=resultado_receitas )
        else:
            return render_template('perfil.html', resultado=resultado, resultado_receitas=resultado_receitas)
    else:
        return redirect(url_for("pagina_inicial"))


@app.route('/perfil/<int:id_usuario>/receitas/<int:pagina>')
def usuario_receita(id_usuario, pagina):
    cursor = database_connection.cursor()
    consulta_receita = 'SELECT * FROM receitas WHERE AutorID = %s'
    cursor.execute(consulta_receita, (id_usuario,))
    resultado = cursor.fetchall()
    inicio_pagina = (pagina-1)*10
    fim_pagina = pagina*10
    resultado_receita= resultado[inicio_pagina:fim_pagina]
    if len(resultado_receita) >0:
        return render_template('usuario_receitas.html', resultado_receita=resultado_receita)
    else:
        return redirect(url_for('pagina_perfil', id_usuario=id_usuario))


@app.route('/cadastro_receita', methods=['GET', 'POST'])
def cadastro_receita():
    if 'user' in session:
        form = FormularioReceita()
        if form.validate_on_submit():
            imagem_receita = form.imagem_receita.data
            formato_imagem = ('.png', '.jpg', '.jpeg')
            if any(imagem_receita.endswith(formato_imagem) for formato in formato_imagem):
                arquivo = secure_filename(imagem_receita.filename)
                caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo)
                with open(imagem_receita, 'rb') as f:
                    f.save(caminho_completo)
            else:
                if imagem_receita:
                    flash("O arquivo não termina com nenhum dos sufixos especificados.")
                    return redirect(url_for('cadastro_receita'))
                else:
                    print('Upload feito sem imagem')
            titulo_receita = form.titulo_receita.data
            descricao_redeita = form.descricao_receita.data
            instrucoes_redeita = form.instrucoes_receita.data
            ingredientes_receita = form.ingredientes_receita.data
            dificuldade_receita = form.dificuldade_receita.data
            tempo_preparo = form.tempo_preparo.data
            categoria_receita = form.categoria_receita.data
            cursor = database_connection.cursor()
            consulta_categoria = 'SELECT * FROM categorias WHERE  categoriaNome= %s'
            cursor.execute(consulta_categoria, (categoria_receita,))
            resultado = cursor.fetchall()
            if resultado:
                id_categoria = resultado[0][0]
                id_usuario = session['user'][0]
                data_postagem = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                inserir_dados = 'INSERT INTO receitas (Titulo, Descricao, Instrucoes, ingredientes, TempoPreparo, Dificuldade, CategoriaID, AutorID, data_hora) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                dados_receita = (titulo_receita, descricao_redeita, instrucoes_redeita, ingredientes_receita, tempo_preparo, dificuldade_receita, id_categoria, id_usuario, data_postagem)
                cursor = database_connection.cursor()
                cursor.execute(inserir_dados, dados_receita)
                database_connection.commit()
                cursor.close()
                flash('Receita Cadastrada com Sucesso')
            else:
                flash('Categoria não Existe')
        return render_template('cadastro_receita.html', form=form)
    else:
        return redirect(url_for('pagina_login'))


@app.route('/logout')
def sair():
    session.pop('user', None)
    return redirect(url_for('pagina_inicial'))


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
