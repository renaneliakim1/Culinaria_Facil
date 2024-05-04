from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField, TextAreaField, FileField, SelectField, DecimalRangeField, RadioField
from flask_wtf.file import FileAllowed
import mysql.connector
from wtforms.widgets import Input



def obter_categorias():
    try:
        database_connection = mysql.connector.connect(user='root', password='', host='localhost',
                                                      database='sitereceita')
        print('Conexão com banco de dados bem sucedida no forms')
        cursor = database_connection.cursor()
        cursor.execute("SELECT categoriaNome FROM categorias")
        categorias = cursor.fetchall()
        cursor.close()
        database_connection.close()
        choices = [(str(categoria[0]), categoria[0]) for categoria in categorias]
        return choices

    except:
        print('Erro ao conectar ao banco de dados no forms')
        return []


class RangeInput500(Input):
    input_type = 'range'
    input_attrs = {'min': '1', 'max': '500'}



class FormularioRegistro(FlaskForm):
    registro_nome = StringField('Nome', validators=[validators.DataRequired()], render_kw={"placeholder": "Nome"})
    registro_email = StringField('Email', validators=[validators.DataRequired(), validators.Email()], render_kw={"placeholder": "E-mail"})
    registro_cpf = StringField('CPF', validators=[validators.DataRequired(), validators.Length(min=11, max=11)], render_kw={"placeholder": "CPF"})
    imagem_perfil = FileField('Imagem do Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])], )
    registro_senha = PasswordField('Senha', validators=[validators.DataRequired(), validators.Length(min=6)], render_kw={"placeholder": "Senha"})
    senha_confirmar = PasswordField('Confirmar Senha', validators=[validators.DataRequired(),
                                                                   validators.EqualTo('registro_senha',
                                                                                      message='As senhas devem corresponder')], render_kw={"placeholder": "Confirmar Senha"})
    submit_registro = SubmitField('Cadastrar')


class FormularioLogin(FlaskForm):
    login_email = StringField('Email', validators=[validators.DataRequired(), validators.Email()],  render_kw={"placeholder": "E-mail"})
    login_senha = PasswordField('Senha', validators=[validators.DataRequired(), validators.Length(min=6)],  render_kw={"placeholder": "Senha"})
    submit_login = SubmitField('Login')




class FormularioReceita(FlaskForm):
    titulo_receita = StringField('Titulo', validators=[ validators.Length(min=3, max=30),validators.DataRequired()], render_kw={"placeholder": "Título da Receita"})
    descricao_receita = TextAreaField('Descricao', validators=[validators.Length(min=3, max=100),validators.DataRequired()], render_kw={"placeholder": "Descreva em até 100 caracteres"})
    instrucoes_receita = TextAreaField('Instrucoes', validators=[validators.DataRequired()], render_kw={"placeholder": "Descreva o passo a passo"})
    ingredientes_receita = TextAreaField('Ingredientes', validators=[validators.DataRequired()], render_kw={"placeholder": "Os ingredientes"})
    tempo_preparo = DecimalRangeField('Tempo de Preparo', default=0)
    dificuldade_receita = RadioField('Dificuldade', choices=[('facil', 'Fácil'), ('medio', 'Médio'), ('dificil', 'Difícil')], validators=[validators.DataRequired()])
    categoria_receita = SelectField('Categoria', choices=obter_categorias, validators=[validators.DataRequired(), validators.InputRequired()])
    imagem_receita = FileField('Imagem da Receita', validators=[ FileAllowed(['jpg', 'png', 'jpeg', 'jfif'])])
    video_receita = FileField('Video Receita', validators=[FileAllowed(["mp4","avi","mkv","mov","wmv","flv","webm","mpeg"])])
    submit_receita = SubmitField('Cadastro_receita')


class FormularioComentario(FlaskForm):
    comentario_receita = TextAreaField('Comentário', validators=[validators.DataRequired()])
    submit_receita = SubmitField('Comentar_receita')


class FormularioPesquisa(FlaskForm):
    pesquisa_input = StringField('Pesquisa', validators=[validators.DataRequired()], render_kw={"placeholder": " Ex: Bolo de Cenoura "})
    submit_receita = SubmitField('Pesquisar')
