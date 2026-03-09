from . import alumnos
from flask import render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
import forms
from models import db, Alumnos as AlumnosModel

csrf = CSRFProtect()


@alumnos.route("/alumnos")
@alumnos.route("/alumnos/index")
def index():
    create_form = forms.UserForm2(request.form)
    alumno_list = AlumnosModel.query.all()
    return render_template("alumnos/index.html", form=create_form, alumno=alumno_list)


@alumnos.route("/alumnos/detalles", methods=["GET"])
def detalles():
    id = request.args.get("id")
    alum1 = db.session.query(AlumnosModel).filter(AlumnosModel.id == id).first()
    if not alum1:
        flash("Alumno no encontrado.", "warning")
        return redirect(url_for("alumnos.index"))

    return render_template(
        "alumnos/detalles.html",
        id=alum1.id,
        nombre=alum1.nombre,
        apallidos=alum1.apallidos,
        email=alum1.email,
        telefono=alum1.telefono,
        cursos=alum1.cursos
    )


@alumnos.route("/alumnos/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm2(request.form)

    if request.method == "GET":
        id = request.args.get("id")
        alum1 = db.session.query(AlumnosModel).filter(AlumnosModel.id == id).first()
        if not alum1:
            flash("Alumno no encontrado.", "warning")
            return redirect(url_for("alumnos.index"))

        create_form.id.data = alum1.id
        create_form.nombre.data = str.rstrip(alum1.nombre)
        create_form.apallidos.data = alum1.apallidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono
        return render_template("alumnos/modificar.html", form=create_form)

    id = create_form.id.data
    alum1 = db.session.query(AlumnosModel).filter(AlumnosModel.id == id).first()

    if alum1:
        alum1.nombre = str.rstrip(create_form.nombre.data)
        alum1.apallidos = create_form.apallidos.data
        alum1.email = create_form.email.data
        alum1.telefono = create_form.telefono.data
        db.session.commit()
        flash("Alumno actualizado correctamente.", "success")
    else:
        flash("Alumno no encontrado.", "warning")

    return redirect(url_for("alumnos.index"))


@csrf.exempt
@alumnos.route("/alumnos/crear", methods=["GET", "POST"])
def crear_alumno():
    create_form = forms.UserForm2(request.form)

    if request.method == "POST":
        alum = AlumnosModel(
            nombre=create_form.nombre.data,
            apallidos=create_form.apallidos.data,
            email=create_form.email.data,
            telefono=create_form.telefono.data
        )
        db.session.add(alum)
        db.session.commit()
        flash("Alumno registrado correctamente.", "success")
        return redirect(url_for("alumnos.index"))

    return render_template("alumnos/Alumnos.html", form=create_form)


@alumnos.route("/alumnos/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.UserForm2(request.form)

    if request.method == "GET":
        id = request.args.get("id")
        alum1 = db.session.query(AlumnosModel).filter(AlumnosModel.id == id).first()

        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = str.rstrip(alum1.nombre)
            create_form.apallidos.data = alum1.apallidos
            create_form.email.data = alum1.email
            create_form.telefono.data = alum1.telefono
        else:
            flash("Alumno no encontrado.", "warning")
            return redirect(url_for("alumnos.index"))

        return render_template("alumnos/eliminar.html", form=create_form)

    id = request.form.get("id") or create_form.id.data
    alum1 = db.session.query(AlumnosModel).filter(AlumnosModel.id == id).first()

    if alum1:
        db.session.delete(alum1)
        db.session.commit()
        flash("Alumno eliminado correctamente.", "danger")
    else:
        flash("Alumno no encontrado.", "warning")

    return redirect(url_for("alumnos.index"))