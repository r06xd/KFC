from models import *
from flask import Flask,render_template,request,flash,g,url_for,redirect
from forms import *
from flask_login import LoginManager, login_user
from flask_bcrypt import check_password_hash
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
    return User.get(user_id)

@app.before_request
def before_request():
    """"Conectar a la base de datos antes de cada request"""
    g.db=models.db
    if g.db.is_closed():
        g.db.connect()

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
        flash(' se creo correctamente')
    return render_template('registro.html',form=formUser)

#<!--Editar para direccionar con las paginas del proyecto-->
@app.route('/login',methods=('GET','POST'))
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
        try:
            user=models.User.get(models.User.username==form.username.data)
        except models.DoesNotExist:
            flash('Tu nombre de usuario o contraseña no existe','error')
        else:#en caso de que el registro si lo encontro en la base
            if check_password_hash(user.password,form.password.data):
                login_user(user)
                flash('Has iniciado sesion','success')
                return redirect(url_for('index'))
    return render_template('login.html',form=form)
#<!--Editar para direccionar con las paginas del proyecto-->

@app.route('/index')
def index():
    return render_template('index.html')

if __name__=='__main__':
    baseDatos()
    app.run(debug=True)
