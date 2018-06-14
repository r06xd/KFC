from models import *
from flask import Flask,render_template,request,flash
from forms import *
from flask_login import LoginManager, login_user
from flask_bcrypt import check_password_hash

app=Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
@app.route('/')
def inicio():
    return render_template('index.html')

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

@app.route('/login',methods=['GET','POST'])
def login():
    formLogin=loginForm(request.form)
    if formLogin.validate_on_submit():
        try:
            user=User.get(username==formLogin.username.data)
        except:
            flash('el usuario o la contraseña son incorrectas')
        else:
            if check_password_hash(User.password,formLogin.password.data):
                login_user(user)
                flash('bienvenido','success')
                return redirect(url_for('inicio'))
    return render_template('login.html',form=formLogin)

if __name__=='__main__':
    baseDatos()
    app.run(debug=True)
