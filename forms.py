from wtforms import Form
from flask_wtf import Form

from wtforms import StringField, IntegerField
from wtforms import EmailField
from wtforms import validators

class UserForm(Form):
    matricula=IntegerField("Matricula", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=100, max=1000, message="Ingrese valor valido")
    ])
    nombre=StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=3, max=10, message="Ingrese nombre valido")
    ])
    apaterno=StringField("APaterno", [
        validators.DataRequired(message="El campo es requerido")
    ])
    amaterno=StringField("AMaterno", [
        validators.DataRequired(message="El campo es requerido")
    ])
    correo=EmailField("Correo", [
        validators.Email(message="Ingresa correo valido")
    ])

class UserForm2(Form):
    id=IntegerField('id',
    [validators.number_range(min=1, max=20, message="valor no valido")
    ])
    nombre=StringField('Nombre', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.length(min=4, max=20, message="requiere min=4 max=20")
    ])
    apaterno=StringField('apaterno', [
        validators.DataRequired(message="El apellido es requerido")
    ])
    email=EmailField('correo', [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo valido")
    ])