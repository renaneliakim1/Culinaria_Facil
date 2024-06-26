from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from forms import FormularioRegistro, FormularioLogin, FormularioReceita, FormularioComentario, FormularioPesquisa
import mysql.connector
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import hashlib
import uuid
import email_validator
import unicodedata
import math


try:
    database_connection = mysql.connector.connect(user='root', password='', host='localhost', database='sitereceita')
    print('Conexão com banco de dados bem sucedida')
except:
    print('Erro ao conectar ao banco de dados')


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = '34#%#$tFDBXCBGHThfd4¨%$28*(86'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpeg']





@app.route('/', methods=['GET', 'POST'])
def pagina_inicial():
    cursor = database_connection.cursor()
    consulta_receitas = 'SELECT * FROM  receitas ORDER BY data_hora DESC LIMIT 3'
    cursor.execute(consulta_receitas)
    resultado_receita = cursor.fetchall()
    cursor.close()
    form_pesquisa = FormularioPesquisa()
    if form_pesquisa.validate_on_submit():
        input_pesquisa = form_pesquisa.pesquisa_input.data
        input_categoria = form_pesquisa.categoria_receita.data
        return redirect( url_for('pagina_pesquisa', input_pesquisa=input_pesquisa,input_categoria=input_categoria, pagina=1))
    if 'user' in session:
        return render_template('index.html', user=session['user'], resultado_receita=resultado_receita, form_pesquisa=form_pesquisa)
    else:
        return render_template('index.html', resultado_receita=resultado_receita, form_pesquisa=form_pesquisa)



@app.route('/receitas/pesquisa/<input_pesquisa>/<input_categoria>/<int:pagina>', methods=['GET', 'POST'])
def pagina_pesquisa(pagina, input_pesquisa, input_categoria):
    cursor = database_connection.cursor()
    pesquisa = input_pesquisa
    if input_categoria == 'todas':
        pesquisa_receita = '''
            SELECT * 
            FROM receitas 
            WHERE Titulo LIKE %s 
            OR Descricao LIKE %s 
            OR Instrucoes LIKE %s 
            OR ingredientes LIKE %s 
            OR TempoPreparo LIKE %s 
            OR Dificuldade LIKE %s
            '''
        cursor.execute(pesquisa_receita, (f'%{pesquisa}%',) * 6)
    else:
        cursor2 = database_connection.cursor()
        categoria_pesquisa = " Select categoriaID from categorias where categoriaNome = %s"
        pesquisa_categoria = input_categoria
        cursor2.execute(categoria_pesquisa, (pesquisa_categoria,))
        resultado_categoria = cursor2.fetchall()
        print(resultado_categoria[0][0])
        categoria_id = resultado_categoria[0][0]
        cursor2.close()
        pesquisa_receita = '''
            SELECT * 
            FROM receitas 
            WHERE CategoriaID = %s
            AND (Titulo LIKE %s 
            OR Descricao LIKE %s 
            OR Instrucoes LIKE %s 
            OR ingredientes LIKE %s 
            OR TempoPreparo LIKE %s 
            OR Dificuldade LIKE %s)
        '''
        cursor.execute(pesquisa_receita, (categoria_id,) + (f'%{pesquisa}%',) * 6)
    resultado_pesquisa = cursor.fetchall()
    cursor.close()
    inicio_pagina = (pagina-1)*10
    fim_pagina = pagina*10
    resultado_receita= resultado_pesquisa [inicio_pagina:fim_pagina]
    form_pesquisa = FormularioPesquisa()
    if form_pesquisa.validate_on_submit():
        input_pesquisa = form_pesquisa.pesquisa_input.data
        input_categoria = form_pesquisa.categoria_receita.data
        return redirect( url_for('pagina_pesquisa', input_pesquisa=input_pesquisa,input_categoria=input_categoria, pagina=1))
    if 'user' in session:
        return render_template('receitas.html', resultado_receita=resultado_receita, pagina=pagina, form_pesquisa=form_pesquisa, user=session['user'], nome_categoria=input_categoria)
    else:
        return render_template('receitas.html', resultado_receita=resultado_receita, pagina=pagina, form_pesquisa=form_pesquisa,  nome_categoria=input_categoria)

@app.route('/receitas/<int:pagina>' , methods=['GET', 'POST'])
def pagina_receitas(pagina):
    cursor = database_connection.cursor()
    consulta_receitas = 'SELECT * FROM receitas ORDER BY data_hora DESC'
    cursor.execute(consulta_receitas)
    resultado = cursor.fetchall()
    inicio_pagina = (pagina-1)*10
    fim_pagina = pagina*10
    resultado_receita= resultado[inicio_pagina:fim_pagina]
    resultado_total = resultado
    form_pesquisa = FormularioPesquisa()
    if form_pesquisa.validate_on_submit():
        input_pesquisa = form_pesquisa.pesquisa_input.data
        input_categoria = form_pesquisa.categoria_receita.data
        return redirect( url_for('pagina_pesquisa', input_pesquisa=input_pesquisa,input_categoria=input_categoria, pagina=1))
    if len(resultado_receita) >0:
        numero_paginas  = list(range(1,math.ceil(len(resultado_total)/10)+1))
        print(numero_paginas)
        print(len(resultado_total))
        math.ceil(len(resultado_total)/10)
        if 'user' in session:
            return render_template('receitas.html', resultado_receita=resultado_receita, pagina=pagina, form_pesquisa=form_pesquisa, user=session['user'], numero_paginas=numero_paginas)
        else:
            return render_template('receitas.html', resultado_receita=resultado_receita, pagina=pagina, form_pesquisa=form_pesquisa, numero_paginas=numero_paginas)
    else:
        return redirect(url_for('pagina_inicial'))


@app.route('/receita/<int:receita_id>', methods=['GET', 'POST'])
def pagina_receita(receita_id):
    cursor = database_connection.cursor()
    consulta_receita = 'SELECT receitaID, Titulo, receitas.descricao, Instrucoes, ingredientes, tempoPreparo, Dificuldade, usuario.nome, usuario.id, data_hora, imagem_receita, video_receita, categoriaNome FROM receitas inner join usuario  on receitas.autorID = usuario.id inner join categorias on categorias.categoriaID = receitas.categoriaID WHERE receitaID = %s'
    cursor.execute(consulta_receita, (receita_id,))
    resultado_receita = cursor.fetchall()
    cursor.close()
    cursor3 = database_connection.cursor()
    consulta_receita = 'SELECT usuario.id, usuario.nome, comentario, data_hora, imagem_perfil FROM comentarios INNER JOIN usuario ON comentarios.usuarioID = usuario.id WHERE receitaID = %s ORDER BY data_hora DESC'
    cursor3.execute(consulta_receita, (receita_id,))
    resultado_comentarios = cursor3.fetchall()
    cursor3.close()
    form_pesquisa = FormularioPesquisa()
    if form_pesquisa.validate_on_submit():
        input_pesquisa = form_pesquisa.pesquisa_input.data
        input_categoria = form_pesquisa.categoria_receita.data
        return redirect( url_for('pagina_pesquisa', input_pesquisa=input_pesquisa,input_categoria=input_categoria, pagina=1))
    if 'user' in session:
        form = FormularioComentario()
        if form.validate_on_submit():
            comentario = form.comentario_receita.data
            data_postagem = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            inserir_comentario = 'INSERT INTO comentarios(receitaID, usuarioID, comentario ,data_hora) VALUES (%s, %s, %s, %s)'
            dados_comentario = (receita_id, session['user'][0],comentario, data_postagem)
            cursor2 = database_connection.cursor()
            cursor2.execute(inserir_comentario, dados_comentario)
            database_connection.commit()
            return redirect(url_for('pagina_receita',receita_id=receita_id))
        return render_template('receita.html', resultado_receita=resultado_receita, user=session['user'], form=form, resultado_comentarios=resultado_comentarios, form_pesquisa=form_pesquisa)
    else:
        return render_template('receita.html', resultado_receita=resultado_receita, resultado_comentarios=resultado_comentarios, form_pesquisa=form_pesquisa)


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
        resultado_receita = resultado[inicio_pagina:fim_pagina]
        if len(resultado_receita) > 0:
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
            imagem_perfil = form.imagem_perfil.data
            if imagem_perfil:
                upload_imagem = True
            else:
                upload_imagem = False
                flash('Perfil sem foto!')
            registro_nome = form.registro_nome.data
            registro_email = form.registro_email.data
            registro_cpf = form.registro_cpf.data
            registro_senha = form.registro_senha.data
            cursor = database_connection.cursor()
            consulta_email = 'SELECT email,cpf FROM usuario WHERE email = %s or cpf = %s'
            cursor.execute(consulta_email, (registro_email, registro_cpf,))
            resultado = cursor.fetchall()
            cursor.close()
            if resultado:
                flash('Alguns dados únicos da Conta já existe. Tente com outro Email ou CPF ')
                return redirect(url_for('pagina_registro'))
            else:
                if registro_cpf.isnumeric():
                    if upload_imagem:
                        nome_arquivo_original = imagem_perfil.filename
                        nome_arquivo_hash = hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()
                        nome_arquivo = nome_arquivo_hash + nome_arquivo_original[nome_arquivo_original.rfind("."):]
                        nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo).encode('ascii', 'ignore').decode('ascii')
                        
                        arquivo = form.imagem_perfil.data
                        arquivo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_arquivo))

                    else:
                        nome_arquivo = "default_user.jpg"
                    senha_hasheada = bcrypt.generate_password_hash(registro_senha).decode('utf-8')
                    inserir_dados = 'INSERT INTO usuario(nome, email, cpf,imagem_perfil, senha) VALUES (%s, %s, %s, %s, %s)'
                    dados_usuario = (registro_nome, registro_email, registro_cpf, nome_arquivo, senha_hasheada)
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
            consulta_conta = 'SELECT id, nome,email, senha, imagem_perfil FROM usuario WHERE email = %s'
            cursor.execute(consulta_conta, (login_email,))
            resultado = cursor.fetchall()
            cursor.close()
            if resultado:
                id_verificado, nome_verificado, email_verificado, senha_verificada, imagem_perfil_verificada = resultado[0]
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
    consulta_usuario = 'SELECT usuario.id,usuario.nome, usuario.email, usuario.imagem_perfil FROM usuario WHERE  usuario.id= %s'
    cursor.execute(consulta_usuario, (id_usuario,))
    resultado = cursor.fetchall()
    cursor.close()
    form_pesquisa = FormularioPesquisa()
    if form_pesquisa.validate_on_submit():
        input_pesquisa = form_pesquisa.pesquisa_input.data
        input_categoria = form_pesquisa.categoria_receita.data
        return redirect( url_for('pagina_pesquisa', input_pesquisa=input_pesquisa,input_categoria=input_categoria, pagina=1))
    if resultado:
        cursor = database_connection.cursor()
        consulta_receita_usuario = 'SELECT receitaID ,Titulo, Descricao, Instrucoes, ingredientes, TempoPreparo, Dificuldade, data_hora, imagem_receita FROM usuario INNER JOIN receitas ON usuario.id = receitas.AutorID WHERE  usuario.id= %s ORDER BY data_hora DESC LIMIT 3'
        cursor.execute(consulta_receita_usuario, (id_usuario,))
        resultado_receitas = cursor.fetchall()
        cursor.close()
        if 'user' in session:
            return render_template('perfil.html', resultado=resultado, resultado_receitas=resultado_receitas, user=session['user'], form_pesquisa=form_pesquisa )
        else:
            return render_template('perfil.html', resultado=resultado, resultado_receitas=resultado_receitas, form_pesquisa=form_pesquisa)
    else:
        return redirect(url_for("pagina_inicial"))


@app.route('/perfil/<int:id_usuario>/receitas/<int:pagina>')
def usuario_receita(id_usuario, pagina):
    cursor = database_connection.cursor()
    consulta_receita = 'SELECT receitaid,titulo, descricao, data_hora, imagem_receita, usuario.nome FROM receitas  inner join usuario on receitas.autorid = usuario.id WHERE AutorID = %s'
    cursor.execute(consulta_receita, (id_usuario,))
    resultado = cursor.fetchall()
    inicio_pagina = (pagina-1)*10
    fim_pagina = pagina*10
    resultado_receita= resultado[inicio_pagina:fim_pagina]
    cursor.close()
    form_pesquisa = FormularioPesquisa()
    if form_pesquisa.validate_on_submit():
        input_pesquisa = form_pesquisa.pesquisa_input.data
        input_categoria = form_pesquisa.categoria_receita.data
        return redirect( url_for('pagina_pesquisa', input_pesquisa=input_pesquisa,input_categoria=input_categoria, pagina=1))
    if len(resultado_receita) >0:
        if 'user' in session:
            return render_template('usuario_receitas.html', resultado_receita=resultado_receita, user=session['user'], form_pesquisa=form_pesquisa)
        else:
            return render_template('usuario_receitas.html', resultado_receita=resultado_receita, form_pesquisa=form_pesquisa)
    else:
        return redirect(url_for('pagina_perfil', id_usuario=id_usuario))


@app.route('/cadastro_receita', methods=['GET', 'POST'])
def cadastro_receita():
    if 'user' in session:
        form = FormularioReceita()
        form_pesquisa = FormularioPesquisa()
        if form_pesquisa.validate_on_submit():
            input_pesquisa = form_pesquisa.pesquisa_input.data
            return redirect( url_for('pagina_pesquisa', input_pesquisa=input_pesquisa, pagina=1))
        if form.validate_on_submit():
            imagem_receita = form.imagem_receita.data
            video_receita = form.video_receita.data
            if imagem_receita:
                upload_imagem = True
            else:
                upload_imagem = False
                flash('Receita Sem Imagem!')
            if video_receita:
                upload_video = True
            else:
                upload_video = False
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
            cursor.close()
            if resultado:
                if upload_imagem:
                    nome_arquivo_original = imagem_receita.filename
                    nome_arquivo_hash = hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()
                    nome_arquivo = nome_arquivo_hash + nome_arquivo_original[nome_arquivo_original.rfind("."):]
                    nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo).encode('ascii', 'ignore').decode('ascii')
                    
                    arquivo = form.imagem_receita.data
                    arquivo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_arquivo))

                else:
                    nome_arquivo = 'receita_default.jpg'
                if upload_video:
                    nome_arquivo_video_original = video_receita.filename
                    nome_arquivo_video_hash = hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()
                    nome_arquivo_video = nome_arquivo_video_hash + nome_arquivo_video_original[nome_arquivo_video_original.rfind("."):]
                    nome_arquivo_video = unicodedata.normalize('NFKD', nome_arquivo_video).encode('ascii', 'ignore').decode('ascii')
                    
                    arquivo = form.video_receita.data
                    arquivo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_arquivo_video))
                else:
                    nome_arquivo_video = 'sem_video'
                id_categoria = resultado[0][0]
                id_usuario = session['user'][0]
                data_postagem = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                inserir_dados = 'INSERT INTO receitas (Titulo, Descricao, Instrucoes, ingredientes, TempoPreparo, Dificuldade, CategoriaID, AutorID, data_hora, imagem_receita, video_receita) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                dados_receita = (titulo_receita, descricao_redeita, instrucoes_redeita, ingredientes_receita, tempo_preparo, dificuldade_receita, id_categoria, id_usuario, data_postagem, nome_arquivo, nome_arquivo_video)
                cursor = database_connection.cursor()
                cursor.execute(inserir_dados, dados_receita)
                database_connection.commit()
                cursor.close()
                flash('Receita Cadastrada com Sucesso')
                return redirect(url_for('pagina_receitas',pagina=1))
            else:
                flash('Categoria não Existe')
        return render_template('cadastro_receita.html', form=form,  user=session['user'], form_pesquisa=form_pesquisa)
    else:
        return redirect(url_for('pagina_login'))



@app.route('/editar_receita/<int:id_receita_editar>', methods=['GET', 'POST'] )
def editar_receita(id_receita_editar):
    if 'user' in session:
        cursor = database_connection.cursor()
        consulta_receita = 'SELECT * FROM receitas inner join categorias on receitas.categoriaid = categorias.categoriaid WHERE ReceitaID= %s'
        cursor.execute(consulta_receita, (id_receita_editar,))
        resultado_receita = cursor.fetchall()
        cursor.close()
        if session['user'][0] == resultado_receita[0][8]:
            form = FormularioReceita(titulo_receita=resultado_receita[0][1], descricao_receita=resultado_receita[0][2],
                                     instrucoes_receita=resultado_receita[0][3], ingredientes_receita=resultado_receita[0][4],
                                     tempo_preparo=resultado_receita[0][5], dificuldade_receita=resultado_receita[0][6],
                                     categoria_receita=resultado_receita[0][12], imagem_receita=resultado_receita[0][10],
                                     video_receita=resultado_receita[0][11])
            
            form_pesquisa = FormularioPesquisa()
            if form_pesquisa.validate_on_submit():
                input_pesquisa = form_pesquisa.pesquisa_input.data
                return redirect( url_for('pagina_pesquisa', input_pesquisa=input_pesquisa, pagina=1))
            if form.validate_on_submit():
                print(resultado_receita[0][10])
                cursor3 = database_connection.cursor()
                categoria_receita = form.categoria_receita.data
                consulta_categoria = 'SELECT * FROM categorias WHERE  categoriaNome= %s'
                cursor3.execute(consulta_categoria, (categoria_receita,))
                categoria_resultado = cursor3.fetchall()
                cursor3.close()
                if categoria_resultado:
                    imagem_receita = resultado_receita[0][10]
                    video_receita = resultado_receita[0][11]
                    if form.imagem_receita.data.filename:
                        nova_upload_imagem = True
                        nova_imagem_receita = form.imagem_receita.data.filename
                        if imagem_receita != nova_imagem_receita:
                            imagem_receita = nova_imagem_receita
                    else:
                        imagem_receita = resultado_receita[0][10]
                        nova_upload_imagem = False
                    if nova_upload_imagem:
                        arquivo_imagem = form.imagem_receita.data
                        nome_arquivo_original = arquivo_imagem.filename
                        nome_arquivo_hash = hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()
                        nome_arquivo = nome_arquivo_hash + nome_arquivo_original[nome_arquivo_original.rfind("."):]
                        nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo).encode('ascii', 'ignore').decode('ascii')
                        
                        arquivo = form.imagem_receita.data
                        arquivo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_arquivo))
                    else:
                        nome_arquivo = resultado_receita[0][10]
                    if form.video_receita.data:
                        novo_upload_video = True
                        novo_video_receita = form.video_receita.data.filename
                        if video_receita != novo_video_receita:
                            video_receita = novo_video_receita
                    else:
                        video_receita = resultado_receita[0][11]
                        novo_upload_video = False
                    if novo_upload_video:
                        arquivo_video = form.video_receita.data
                        nome_arquivo_video_original = arquivo_video.filename
                        nome_arquivo_video_hash = hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()
                        nome_arquivo_video = nome_arquivo_video_hash + nome_arquivo_video_original[nome_arquivo_video_original.rfind("."):]
                        nome_arquivo_video = unicodedata.normalize('NFKD', nome_arquivo_video).encode('ascii', 'ignore').decode('ascii')
                        
                        arquivo = form.video_receita.data
                        arquivo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_arquivo_video))
                    else:
                        nome_arquivo_video = resultado_receita[0][11]

                    categoria_resultado = categoria_resultado[0][0]
                    titulo_receita = form.titulo_receita.data
                    descricao_receita = form.descricao_receita.data
                    instrucoes_receita = form.instrucoes_receita.data
                    ingredientes_receita = form.ingredientes_receita.data
                    tempo_preparo = form.tempo_preparo.data
                    dificuldade_receita = form.dificuldade_receita.data
                    if resultado_receita[0][10] == 'receita_default.jpg' or resultado_receita[0][10] == nome_arquivo:
                        pass
                    else:
                        try:
                            nome_imagem_deletar = resultado_receita[0][10]
                            caminho_deletar_imagem = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_imagem_deletar)
                            os.remove(caminho_deletar_imagem)
                            print('antiga imagem deletada')
                        except:
                            pass
                    if resultado_receita[0][11] == 'sem_video' or resultado_receita[0][11] == nome_arquivo_video:
                        pass
                    else:
                        try:
                            nome_video_deletar = resultado_receita[0][11]
                            caminho_deletar_video = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_video_deletar)
                            os.remove(caminho_deletar_video)
                            print('antigo video deletado')
                        except:
                            pass
                    cursor2 = database_connection.cursor()
                    dados_receita = (titulo_receita, descricao_receita, instrucoes_receita, ingredientes_receita, tempo_preparo, dificuldade_receita, categoria_resultado, nome_arquivo, nome_arquivo_video, id_receita_editar)
                    consulta_receita = 'UPDATE receitas SET Titulo = %s, Descricao = %s, Instrucoes = %s, Ingredientes = %s, TempoPreparo = %s, Dificuldade = %s, CategoriaID = %s, imagem_receita = %s, video_receita = %s WHERE receitaID = %s'
                    cursor2.execute(consulta_receita, dados_receita)
                    database_connection.commit()
                    cursor2.close()
                    return redirect(url_for('pagina_receita', receita_id=id_receita_editar))
                else:
                    flash('Receita não atualizada. Categoria não existe')
                    return redirect(url_for('editar_receita', id_receita_editar=id_receita_editar))
            return render_template('editar_receita.html', resultado_receita=resultado_receita, form=form, form_pesquisa=form_pesquisa, user=session['user'])
    else:
        return redirect(url_for('pagina_inicial'))



@app.route('/editar_perfil/<int:id_usuario>', methods=['GET', 'POST'])
def editar_perfil(id_usuario):
    if 'user' in session:
        cursor = database_connection.cursor()
        consulta_perfil = 'SELECT * FROM usuario WHERE usuario.id= %s'
        cursor.execute(consulta_perfil, (id_usuario,))
        resultado_perfil = cursor.fetchall()
        cursor.close()
        if resultado_perfil:
            if session['user'][0] == resultado_perfil[0][0]:
                form = FormularioRegistro(registro_nome=resultado_perfil[0][1], registro_email=resultado_perfil[0][2],
                                        registro_cpf=resultado_perfil[0][4], imagem_perfil=resultado_perfil[0][5])
                cursor = database_connection.cursor()
                consulta_receita = 'SELECT receitaid,titulo, descricao, data_hora, imagem_receita, usuario.nome FROM receitas  inner join usuario on receitas.autorid = usuario.id WHERE AutorID = %s'
                cursor.execute(consulta_receita, (id_usuario,))
                usuario_receita = cursor.fetchall()
                cursor.close()
                if form.validate_on_submit():
                    imagem_perfil = form.imagem_perfil.data
                    novo_nome = form.registro_nome.data
                    novo_email = form.registro_email.data
                    novo_cpf = form.registro_cpf.data
                    nova_senha = form.registro_senha.data
                    cursor = database_connection.cursor()
                    consulta_email = 'SELECT email,cpf FROM usuario WHERE email = %s and cpf= %s'
                    cursor.execute(consulta_email, (novo_email, novo_cpf))
                    resultado_consulta = cursor.fetchall()
                    cursor.close()
                    if novo_cpf.isnumeric():
                        if resultado_consulta:
                            if resultado_consulta[0][0] == resultado_perfil[0][2] or resultado_consulta[0][1] == resultado_perfil[0][4]:
                                atualizar_perfil = True
                            else:
                                atualizar_perfil = False
                            if atualizar_perfil:
                                if imagem_perfil:
                                    nome_imagem_perfil = form.imagem_perfil.data.filename
                                    novo_upload_imagem = True
                                    if imagem_perfil.filename != nome_imagem_perfil:
                                        pass
                                else:
                                    nome_imagem_perfil = resultado_perfil[0][5]
                                    novo_upload_imagem = False
                                if novo_upload_imagem:

                                    nome_arquivo_original = imagem_perfil.filename
                                    nome_arquivo_hash = hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()
                                    nome_arquivo = nome_arquivo_hash + nome_arquivo_original[nome_arquivo_original.rfind("."):]
                                    nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo).encode('ascii', 'ignore').decode('ascii')
                                    
                                    arquivo = form.imagem_perfil.data
                                    arquivo.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_arquivo))

                                else:
                                    nome_arquivo = resultado_perfil[0][5]
                                senha_hasheada = bcrypt.generate_password_hash(nova_senha).decode('utf-8')
                                cursor3 = database_connection.cursor()
                                consulta_imagem = 'SELECT imagem_perfil FROM usuario WHERE usuario.id= %s'
                                cursor3.execute(consulta_imagem, (id_usuario,))
                                resultado_imagem = cursor3.fetchall()
                                cursor3.close()
                                if resultado_imagem:
                                    if resultado_imagem[0][0] == 'default_user.jpg' or resultado_imagem[0][0] == nome_arquivo:
                                        pass
                                    else:

                                        nome_imagem_deletar = resultado_imagem[0][0]
                                        caminho_deletar_imagem = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                                              app.config['UPLOAD_FOLDER'], nome_imagem_deletar)
                                        try:
                                            os.remove(caminho_deletar_imagem)
                                            print('apagado:' + nome_imagem_deletar)
                                        except:
                                            pass
                                cursor2 = database_connection.cursor()
                                atualizar_usuario = 'UPDATE usuario SET nome = %s, email = %s, senha = %s, imagem_perfil = %s where usuario.id= %s '
                                cursor2.execute(atualizar_usuario, (novo_nome, novo_email, senha_hasheada, nome_arquivo, resultado_perfil[0][0]))
                                database_connection.commit()
                                cursor2.close()
                                flash('Faça login novamente para ver as alterações')
                                return redirect(url_for('sair'))
                            else:
                                flash('Credenciais CPF ou email já existe')
                                return redirect(url_for('editar_perfil', id_usuario=id_usuario))
                    else:
                        flash('CPF precisa ser númerico')
                        return redirect(url_for('editar_perfil', id_usuario=id_usuario))
                return render_template('editar_perfil.html', form=form, user=session['user'], usuario_receita=usuario_receita)
            else:
                return redirect(url_for('pagina_inicial'))
        else:
            return redirect(url_for('pagina_inicial'))
    else:
        return redirect(url_for('pagina_inicial'))


@app.route('/dicas' , methods=['GET', 'POST'])
def dicas():
    form_pesquisa = FormularioPesquisa()
    if form_pesquisa.validate_on_submit():
        input_pesquisa = form_pesquisa.pesquisa_input.data
        input_categoria = form_pesquisa.categoria_receita.data
        return redirect( url_for('pagina_pesquisa', input_pesquisa=input_pesquisa,input_categoria=input_categoria, pagina=1))
    if 'user' in session:
        return render_template('dicas.html', user=session['user'], form_pesquisa=form_pesquisa)
    else:
        return render_template('dicas.html', form_pesquisa=form_pesquisa)
    




@app.route('/logout')
def sair():
    session.pop('user', None)
    return redirect(url_for('pagina_inicial'))




'''if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)'''



if __name__ == "__main__":
        app.run(debug='True', host='0.0.0.0', port=5000)

