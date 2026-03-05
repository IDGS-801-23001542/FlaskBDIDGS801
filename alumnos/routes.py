from . import alumnos
from flask import render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
import forms
from models import db, Alumnos as AlumnosModel

csrf = CSRFProtect()

@alumnos.route("/")
@alumnos.route("/index")
def index():
    create_form = forms.UserForm2(request.form)
    alumno_list = AlumnosModel.query.all()
    return render_template("index.html", form=create_form, alumno=alumno_list)


@alumnos.route('/detalles', methods=['GET', 'POST'])
def detalles():
    create_form = forms.UserForm2(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(AlumnosModel).filter(AlumnosModel.id == id).first()

        if not alum1:
            return redirect(url_for('alumnos.index'))

        return render_template(
            'detalles.html',
            id=alum1.id,
            nombre=alum1.nombre,
            apallidos=alum1.apallidos,
            email=alum1.email,
            telefono=alum1.telefono
        )


@alumnos.route('/modificar', methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm2(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(AlumnosModel).filter(AlumnosModel.id == id).first()

        if not alum1:
            return redirect(url_for('alumnos.index'))

        create_form.id.data = alum1.id
        create_form.nombre.data = str.rstrip(alum1.nombre)
        create_form.apallidos.data = alum1.apallidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono

        return render_template('modificar.html', form=create_form)

    if request.method == 'POST':
        id = create_form.id.data
        alum1 = db.session.query(AlumnosModel).filter(AlumnosModel.id == id).first()

        if alum1:
            alum1.nombre = str.rstrip(create_form.nombre.data)
            alum1.apallidos = create_form.apallidos.data
            alum1.email = create_form.email.data
            alum1.telefono = create_form.telefono.data

            db.session.add(alum1)
            db.session.commit()

        return redirect(url_for('alumnos.index'))

    return render_template('modificar.html', form=create_form)


@csrf.exempt
@alumnos.route("/alumnos", methods=['GET', 'POST'])
def Alumnos():
    create_form = forms.UserForm2(request.form)

    if request.method == 'POST':
        alum = AlumnosModel(
            nombre=create_form.nombre.data,
            apallidos=create_form.apallidos.data,
            email=create_form.email.data,
            telefono=create_form.telefono.data
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumnos.index'))

    return render_template("Alumnos.html")


@alumnos.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm2(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(AlumnosModel).filter(AlumnosModel.id == id).first()

        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = str.rstrip(alum1.nombre)
            create_form.apallidos.data = alum1.apallidos
            create_form.email.data = alum1.email
            create_form.telefono.data = alum1.telefono

        return render_template('eliminar.html', form=create_form)

    if request.method == 'POST':
        id = request.form.get('id') or create_form.id.data
        alum1 = db.session.query(AlumnosModel).filter(AlumnosModel.id == id).first()

        if alum1:
            db.session.delete(alum1)
            db.session.commit()

        return redirect(url_for('alumnos.index'))

    return render_template('eliminar.html', form=create_form)