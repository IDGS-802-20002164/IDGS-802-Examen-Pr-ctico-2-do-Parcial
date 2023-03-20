from flask import Blueprint, render_template,request,flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_accepted, roles_required
from . import db
from . import forms

main = Blueprint('main', __name__)

#Definimos la ruta para la página principal
@main.route('/')
def index():
    return render_template('indexsin.html')

#Definimos la ruta para la página de perfil de usuario
@main.route('/profile')
@login_required
def profile():
    form = forms.UserForm(request.form)
    if request.method == 'POST':
        flash('Eliminacion Exitosa!!!')
   
    return render_template('profile.html', name = current_user.name,form=form)