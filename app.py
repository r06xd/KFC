from models import *
from flask import Flask,render_template,request,flash,g,url_for,redirect
from forms import *
from flask_login import LoginManager, login_user,current_user
from flask_bcrypt import check_password_hash,generate_password_hash
import forms
import models

DEBUG=True
PORT=7000
HOST='0.0.0.0'

app=Flask(__name__)
app.config.from_object(__name__)

#<!--Editar para direccionar con las paginas del proyecto-->

app.secret_key='jhsakdJKHyjkdjksadA@2345''!klsjdkjh23456dfdgd'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

#metodo para cargar el usuario q esta logiado
#<!--Editar para direccionar con las paginas del proyecto-->
#se agrego el user loeader para que funcione
@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id==user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """"Conectar a la base de datos antes de cada request"""
    g.db=models.db
    if g.db.is_closed():
        g.db.connect()
        g.user = current_user


@app.after_request
def after_request(response):
    """Cerramos la conexion a la base de datos"""
    g.db.close()
    return response

@app.route('/principal')
def principal():
    return render_template('principal.html')

@app.route('/registro',methods=['GET','POST'])
def registro():
    formUser=user(request.form)
    if request.method =='POST' and formUser.validate():
        User.create_user(
        nombre=formUser.nombre.data,
        apellido=formUser.apellido.data,
        username=formUser.username.data,
        password=formUser.password.data
        )
        return redirect(url_for('login'))
    return render_template('registro.html',form=formUser)

#<!--Editar para direccionar con las paginas del proyecto-->
@app.route('/',methods=('GET','POST'))
@app.route('/login',methods=('GET','POST'))
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
        try:
            user=models.User.get(models.User.username==form.username.data)
            print('XXXXXentro y encontro usuario')
        except models.DoesNotExist:
            print('XXXXXno encontro usuario')
            flash('Tu nombre de usuario o contraseña no existe','error')
        else:
            if check_password_hash(user.password,form.password.data):
                login_user(user)
                print('XXXXXXXXentro a buscar url')
                flash('Has iniciado sesion','success')
                return redirect(url_for('index'))
            else:
                flash('Tu nombre de usuario o contraseña no existe','error')
    return render_template('login.html',form=form)

#<!--Editar para direccionar con las paginas del proyecto-->

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/pedidoCrear',methods=['GET','POST'])
def pedidoCrear():
    formPedido=forms.pedido(request.form)
    if request.method=='POST' and formPedido.validate():
        models.pedido.create_Pedido(
        cliente=formPedido.cliente.data,
        usuarioLog=g.user.id,
        descripcion=formPedido.descripcion.data,
        valor=formPedido.valor.data
        )
        flash('se guardo correctamente')
    return render_template('pedido.html',form=formPedido)
@app.route('/logout')
def logout():
    return redirect('login')

@app.route('/buscarUsuario')
def buscarUsuario():
    usuarioEncontrado=""
    listaUsuario=User.select()
    listUser=[]
    if g.user.username!='admin':
        idEditar=g.user.id
    try:
        usuarioEncontrado=User.get(id=idEditar)
        print('entro correctamente')
    except:
        print('usuerio logeado no existe')
    for usuario in listaUsuario:
        listUser.append(usuario)
    return render_template('buscar.html',lista=listUser,usuarioEditar=usuarioEncontrado)

@app.route('/editar',methods=['GET','POST'])
def editar(usuario=""):
    usuarioEncontrado=""
    listaUsuario=User.select()
    listUser=[]
    for usuario in listaUsuario:
        listUser.append(usuario)
    idUsuerio=request.form.get('SelectUser')
    idEditar=request.form.get('idF')

    print('------>>> dato obtenido',idUsuerio)
    print('------>>> dato obtenido editar',g.user.username)
    print('++++++ dato post botones',request.form.get('btn'))
    try:
        usuarioEncontrado=User.get(id=idUsuerio)
        usuarioAEditar=User.get(id=idEditar)
        print(usuarioAEditar.id)
        print(g.user.username)
    except:
        print('usuario no existe')

    if request.form.get('btn')=='Guardar':
        try:
            print('ingrese el nombre del usuario')
            nombreI=request.form.get('nombreF')
            print('===>>>',nombreI)
            if not nombreI:
                print('is none')
                nombreI=usuarioEncontrado.nombre
            print('ingrese el apellido del usuario')
            apellidoI=request.form.get('apellidoF')
            print('===>>>',apellidoI)
            if not apellidoI:
                apellidoI=usuarioEncontrado.apellido
            print('ingrese el username')
            usernameI=request.form.get('usernameF')
            if not usernameI:
                usernameI=usuarioEncontrado.username
            print('desea guardar los datos ingresados?')
            opcion='y'
            if(opcion=='y'):
                query=User.update(
                nombre=nombreI,
                apellido=apellidoI,
                username=usernameI,
                ).where(User.id==usuarioAEditar.id)
                query.execute()
                regresar=(""+
                            "<form method='POST' action='/editar'> "+
                            "se guardo correctamente </br>"+
                            "<input type='submit' value='Regresar'> "+
                            "</form> ")
                return regresar
            else:
                print('no se creo el usuario')
        except:
            print('no existe el usuario')
    return render_template('buscar.html',lista=listUser,usuarioEditar=usuarioEncontrado)

@app.route('/listaPedidos',methods=['GET','POST'])
def pedidoUsuarios():
    print(g.user.id)
    pedidoListado=models.pedido.select().where(models.pedido.usuarioLog==g.user.id)
    print(pedidoListado[0].descripcion)
    listaPedidos=[]
    for pedidos in pedidoListado:
        listaPedidos.append(pedidos)
    return render_template('pedidoLista.html',lista=listaPedidos)


if __name__=='__main__':
    baseDatos()
    app.run(debug=True)
