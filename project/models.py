#Importamos el objeto de la base de datos __init__.py
from . import db
from flask_sqlalchemy import SQLAlchemy
#Importamos la clase UserMixin de  flask_login
from flask_security import UserMixin, RoleMixin

user_roles = db.Table('users_roles',
db.Column('userId', db.Integer, db.ForeignKey('user.id')),
db.Column('roleId', db.Integer, db.ForeignKey('role.id')))


class User(UserMixin, db.Model):
    """User account model.""" 
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role',
      secondary = user_roles,
      backref = db.backref('users', lazy = 'dynamic'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class VideoJuegos(db.Model, RoleMixin):
    __tablename__ = 'videoJuegos'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    unidades = db.Column(db.INTEGER())




