from wtforms import Form
from wtforms import StringField, IntegerField, EmailField, TextAreaField
from wtforms import validators

class UserForm2(Form):
    id = IntegerField('id', [
        validators.NumberRange(min=1, max=999999, message="valor no valido")
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=4, max=20, message="requiere min=4 max=20")
    ])
    apallidos = StringField('apallidos', [
        validators.DataRequired(message="Los apellidos son requeridos"),
        validators.Length(min=3, max=200, message="requiere min=3 max=200")
    ])
    email = EmailField('email', [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo valido")
    ])
    telefono = StringField('telefono', [
        validators.DataRequired(message="El telefono es requerido"),
        validators.Length(min=7, max=20, message="requiere min=7 max=20")
    ])

class MaestroForm(Form):
    matricula = IntegerField("Matricula", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=100, max=999999, message="Ingrese valor valido")
    ])
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=3, max=50, message="Ingrese nombre valido")
    ])
    apellidos = StringField("Apellidos", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=3, max=50, message="Ingrese apellidos validos")
    ])
    especialidad = StringField("Especialidad", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=3, max=50, message="Ingrese especialidad valida")
    ])
    email = EmailField("Email", [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo valido")
    ])

class CursoForm(Form):
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=3, max=150, message="min 3 max 150")
    ])
    descripcion = TextAreaField("Descripcion")
    maestro_id = IntegerField("Maestro", [
        validators.DataRequired(message="Seleccione un maestro")
    ])

class InscripcionForm(Form):
    alumno_id = IntegerField("Alumno", [validators.DataRequired()])
    curso_id = IntegerField("Curso", [validators.DataRequired()])