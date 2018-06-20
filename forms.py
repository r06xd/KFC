from wtforms import Form,StringField,BooleanField, IntegerField, PasswordField, validators,SelectField, TextAreaField
from flask_wtf import FlaskForm
from models import *
from wtforms.validators import (DataRequired, ValidationError, Email, Regexp,
                                Length, EqualTo)

class user(FlaskForm):
    nombre=StringField()
    apellido=StringField()
    username=StringField()
    password=PasswordField('password',[validators.DataRequired(),validators.EqualTo('confirm',message='es incorrecto')])
    confirm=PasswordField('confirme')

class pedido(FlaskForm):
    cliente=StringField()
    descripcion=StringField()
    valor=StringField()

#<!--Editar para direccionar con las paginas del proyecto-->
#formulario de iniciar sesión
class LoginForm(FlaskForm):
    username=StringField(
        'Email',
        validators=[

            DataRequired(),
        ])
    password=PasswordField(
        'Password',
        validators=[
            DataRequired(),
            ])


class PostForm(FlaskForm):
    content=TextAreaField(
        'Que piensas',
        validators=[
            DataRequired()
        ]
    )
