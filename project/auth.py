from flask import Blueprint, render_template, url_for, request, flash, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from .models import User , user_roles, VideoJuegos
from . import db, userDataStore
from .temApp import getAllTabla, getAllName, buy,insertJuego
from . import forms
import base64
from io import BytesIO
import io
from PIL import Image
import zlib

auth = Blueprint('auth', __name__, url_prefix = '/security')

@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    form = forms.UserForm(request.form)
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #Consultamos si existe un usuario ya registrado con ese email
    user = User.query.filter_by(email=email).first()
    #roles = User.query.filter_by(roles=roles).first()
    
   

    #Verificamos si el usuario existe y comprobamos el password
    if not user or not check_password_hash(user.password, password):
        flash('El usuario y/o contraseña son inconrrectos')
        return redirect(url_for('auth.login',form=form)) # Rebotamos a la pagina de login

    #Si llegamos aqui los datos son correctos y creamos una session para el usuario
    login_user(user, remember=remember)

    if str(user.roles) == '[<Role 1>]':
        return  render_template('indexAdm.html')
    else:
        return  render_template('index.html')

    return redirect(url_for('main.profile'))

@auth.route('/register')
def register():
    return render_template('/security/register.html')



@auth.route('/catalogo', methods=['GET','POST'])
def catalogo():
    btn5 = request.form.get("buscarID")
    form = forms.UserForm(request.form)
    maestr = getAllTabla.getall()

    if request.method=='POST':
        if btn5 == 'Buscar':
            id= form.buscar.data
            if id != '':
                maestr = getAllName.getallName(id)
                
    
    return render_template('catalogo.html',maestr=maestr,form=form)

@auth.route('/catalogoAdm', methods=['GET','POST'])
def catalogoAdm():
    btn5 = request.form.get("buscarID")
    btn6 = request.form.get("Agregar")
    btn7 = request.form.get("Eliminar")
    form = forms.UserForm(request.form)
    maestr = getAllTabla.getall()

    if request.method=='POST':
        if btn5 == 'Buscar':
            id= form.buscar.data
            if id != '':
                maestr = getAllName.getallName(id)
        if btn6 == 'Agregar Juego':
            return redirect(url_for('auth.agregar'))
        if btn7 == 'Eliminar Juego':
            return redirect(url_for('auth.eliminar'))

                
    
    return render_template('catalogoAdm.html',maestr=maestr,form=form)

@auth.route('/agregar', methods=['GET','POST'])
def agregar():
    btn = request.form.get("registrar")
    create_form = forms.UserForm(request.form)
    if request.method=='POST':

        if btn == 'Registrar Juego':
            name= create_form.name.data
            description = create_form.description.data
            unidades = create_form.unidades.data
            
            insertJuego.insertjuego(name, description, upload_image(), unidades)
            return redirect(url_for('auth.catalogoAdm'))
    return render_template('agregar.html',form=create_form)

@auth.route('/eliminar', methods=['GET','POST'])
def eliminar():
    create_fprm= forms.UserForm(request.form)
    btn5 = request.form.get("comprar")
    if request.method == 'GET':
        create_fprm= forms.UserForm(request.form)
        id=request.args.get('id')
        alum1=db.session.query(VideoJuegos).filter(VideoJuegos.id == id).first()
        create_fprm.id.data=request.args.get('id')
        create_fprm.name.data= alum1.name
        create_fprm.description.data= alum1.description
        create_fprm.unidades.data= alum1.unidades
    if request.method == 'POST':
        id = create_fprm.id.data
        maes = db.session.query(VideoJuegos).filter(VideoJuegos.id==id).first()
        unidad = create_fprm.unidades.data
        db.session.delete(maes)
        db.session.commit()
        flash('Eliminacion Exitosa!!!')
    return render_template('eliminar.html',form=create_fprm)

@auth.route('/modificar', methods=['GET','POST'])
def modificar():
    create_fprm= forms.UserForm(request.form)
    if request.method == 'GET':
        create_fprm= forms.UserForm(request.form)
        id=request.args.get('id')
        alum1=db.session.query(VideoJuegos).filter(VideoJuegos.id == id).first()
        create_fprm.id.data=request.args.get('id')
        create_fprm.name.data= alum1.name
        create_fprm.description.data= alum1.description
        create_fprm.unidades.data= alum1.unidades
    if request.method == 'POST':
        id = create_fprm.id.data
        maes = db.session.query(VideoJuegos).filter(VideoJuegos.id==id).first()
        maes.unidades = create_fprm.unidades.data
        maes.name = create_fprm.name.data
        maes.description = create_fprm.description.data
        db.session.add(maes)
        db.session.commit()
        
        flash('Modificacion Exitosa!!!')
    return render_template('modificar.html',form=create_fprm)



def upload_image():
   
    image_file = request.files["image"]
    
    # Convertir la imagen a un objeto Pillow
    img = Image.open(image_file)

    # Codificar la imagen en base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Enviar la respuesta de vuelta a HTML
    return encoded_string





@auth.route('/comprar', methods=['GET','POST'])
def comprar():
    create_fprm= forms.UserForm(request.form)
    btn5 = request.form.get("comprar")
    if request.method == 'GET':
        create_fprm= forms.UserForm(request.form)
        id=request.args.get('id')
        alum1=db.session.query(VideoJuegos).filter(VideoJuegos.id == id).first()
        create_fprm.id.data=request.args.get('id')
        create_fprm.nombre.data= alum1.name
        create_fprm.apellidos.data= alum1.description
        create_fprm.buscar.data= alum1.unidades
    if request.method == 'POST':
        id = create_fprm.id.data
        maes = db.session.query(VideoJuegos).filter(VideoJuegos.id==id).first()
        unidad = create_fprm.buscar.data
        maes.unidades = int(unidad)-1
        db.session.add(maes)
        db.session.commit()
        flash('Compra Exitosa!!!')
        
    
    return render_template('compra.html',form=create_fprm)



@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    #Consultamos si existe un usuario ya registrado con ese email
    user = User.query.filter_by(email=email).first()

    if user:
        flash('El correo ya se encuentra en uso')
        return redirect(url_for('auth.register'))

    userDataStore.create_user(name = name, email = email, password = generate_password_hash
    (password, method = 'sha256'))

    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    #Cerramos sesión
    logout_user()
    return redirect(url_for('main.index'))
