from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms import EmailField
from wtforms import validators

class UserForm(Form):
    id=IntegerField('id')
    nombre = StringField('nombre')
    apellidos=StringField('apellidos')
    email=EmailField('correo')
    buscar=StringField('Buscar por Id')
    name = StringField('name')
    description=StringField('description')
    img=StringField('img')
    unidades=IntegerField('unidades')
    motivo=StringField('motivo')
    descripcion = StringField('descripcion')
    


    