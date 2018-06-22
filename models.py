from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from flask import flash
db=SqliteDatabase('kfc.db')

#clase de usuario
class User(UserMixin,Model):
    nombre=CharField()
    apellido=CharField()
    username=CharField(unique=True)
    password=CharField()
    class Meta:
        database=db
    @classmethod #metodo de la clase para registrar el usuario
    def create_user(cls,nombre,apellido,username,password):
        try:
            cls.create(
            nombre=nombre,
            apellido=apellido,
            username=username,
            password=generate_password_hash(password)
            )
            flash(' se creo correctamente')
        except IntegrityError:
            return flash('usuario ya existe')

#clase de pedido
class pedido(Model):
    cliente=CharField()
    usuarioLog=ForeignKeyField(User)
    descripcion=CharField()
    valor=CharField()
    class Meta:
        database=db
    @classmethod #metodo de la clase para crear el pedido
    def create_Pedido(cls,cliente,usuarioLog,descripcion,valor):
        try:
            cls.create(
            cliente=cliente,
            usuarioLog=usuarioLog,
            descripcion=descripcion,
            valor=valor
            )
        except IntegrityError:
            raise ValueError('el pedido ya existe')

#metodo que crea las tablas antes definidas
def baseDatos():
    db.connect()
    db.create_tables([User,pedido],safe=True)
    db.close()
