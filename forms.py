from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField, TextAreaField, IntegerField

class FormularioRegistro(FlaskForm):
    registro_nome = StringField('Nome', validators=[validators.DataRequired()])
    registro_email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    registro_senha = PasswordField('Senha', validators=[validators.DataRequired(), validators.Length(min=6)])
    senha_confirmar = PasswordField('Confirmar Senha', validators=[validators.DataRequired(),
                                                                   validators.EqualTo('registro_senha',
                                                                                      message='As senhas devem corresponder')])
    submit_registro = SubmitField('Registrar')


class FormularioLogin(FlaskForm):
    login_email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    login_senha = PasswordField('Senha', validators=[validators.DataRequired(), validators.Length(min=6)])
    submit_login = SubmitField('Login')


class FormularioReceita(FlaskForm):
    titulo_receita = StringField('Titulo', validators=[validators.DataRequired()])
    descricao_receita = TextAreaField('Descricao', validators=[validators.DataRequired()])
    instrucoes_receita = TextAreaField('Instrucoes', validators=[validators.DataRequired()])
    ingredientes_receita = TextAreaField('Ingredientes', validators=[validators.DataRequired()])
    tempo_preparo = IntegerField('Tempo de Preparo(minutos)', [validators.NumberRange(min=0, max=500)])
    dificuldade_receita = StringField('Dificuldade', validators=[validators.DataRequired()])
    categoria_receita = StringField('Categoria', validators=[validators.DataRequired()])
    submit_receita = SubmitField('Cadastro_receita')





