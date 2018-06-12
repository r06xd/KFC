from peewee import *

db=SqliteDatabase('kfc.db')

class User(Model):
    nombre=CharField()
    apellido=CharField()
    username=CharField()
    password=CharField()
    class Meta:
        database=db
    @ClassMethod
    def create_user(cls,nombre,apellido,username,password):
        try:
            cls.create(
            nombre=nombre,
            apellido=apellido,
            username=username,
            password=password
            )
        except IntegrityError:
            raise ValueError('el usuario ya existe')
class pedido(Model):
    cliente=CharField()
    usuarioLog=ForeignKeyField(User)
    descripcion=CharField()
    valor=CharField()
    class Meta:
        database=db
    @ClassMethod
    def createPedido(cls,descripcion,valor):
        try:
            cls.create(
            descripcion=descripcion,
            valor=valor
            )
        except IntegrityError:
            raise ValueError('el pedido ya existe')

def baseDatos():
    db.connect()
    db.create_tables([User,pedido],safe=True)
    db.close()
