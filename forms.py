from wtforms import Form,StringField,BooleanField, IntegerField, PasswordField, validators,SelectField
from flask_wtf import FlaskForm
from models import *

class user(FlaskForm):
    nombre=StringField()
    apellido=StringField()
    username=StringField()
    password=PasswordField('password',[validators.DataRequired(),validators.EqualTo('confirm',message='es incorrecto')])
    confirm=PasswordField('confirme')

class pedido(FlaskForm):
    cliente=StringField()
    descripcion=StringField()
    valor=IntegerField()

class loginForm(FlaskForm):
    username=StringField()
    password=PasswordField()
