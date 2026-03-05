from . import maestros
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

import forms
from models import db, Maestros as MaestrosModel


@maestros.route('/maestros', methods=['GET', 'POST'])
def listado_maestros():
    create_form = forms.MaestroForm(request.form)

    if request.method == 'POST':
        if hasattr(create_form, "validate") and not create_form.validate():
            flash("Revisa los datos del formulario.", "warning")
            return redirect(url_for('maestros.listado_maestros'))

        matricula = create_form.matricula.data

        existe = MaestrosModel.query.filter_by(matricula=matricula).first()
        if existe:
            flash(f"La matrícula {matricula} ya está registrada.", "warning")
            return redirect(url_for('maestros.listado_maestros'))

        maes = MaestrosModel(
            matricula=matricula,
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data
        )

        try:
            db.session.add(maes)
            db.session.commit()
            flash("Maestro registrado.", "success")
        except IntegrityError:
            db.session.rollback()
            flash(f"La matrícula {matricula} ya está registrada.", "warning")

        return redirect(url_for('maestros.listado_maestros'))

    maes = MaestrosModel.query.all()
    return render_template("maestros/listadoMaes.html", form=create_form, maestros=maes)


@maestros.route('/maestros/detalles', methods=['GET'])
def detalles_maestros():
    matricula = request.args.get('matricula')
    maes1 = MaestrosModel.query.filter_by(matricula=matricula).first()

    if not maes1:
        flash("No se encontró el maestro.", "warning")
        return redirect(url_for('maestros.listado_maestros'))

    return render_template(
        'maestros/detallesMaes.html',
        matricula=maes1.matricula,
        nombre=maes1.nombre,
        apellidos=maes1.apellidos,
        especialidad=maes1.especialidad,
        email=maes1.email
    )


@maestros.route('/maestros/modificar', methods=['GET', 'POST'])
def modificar_maestros():
    create_form = forms.MaestroForm(request.form)

    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maes1 = MaestrosModel.query.filter_by(matricula=matricula).first()

        if not maes1:
            flash("No se encontró el maestro.", "warning")
            return redirect(url_for('maestros.listado_maestros'))

        create_form.matricula.data = maes1.matricula
        create_form.nombre.data = maes1.nombre
        create_form.apellidos.data = maes1.apellidos
        create_form.especialidad.data = maes1.especialidad
        create_form.email.data = maes1.email

        return render_template('maestros/modificarMaes.html', form=create_form)

    # POST
    if hasattr(create_form, "validate") and not create_form.validate():
        flash("Revisa los datos del formulario.", "warning")
        return render_template('maestros/modificarMaes.html', form=create_form)

    matricula = create_form.matricula.data
    maes1 = MaestrosModel.query.filter_by(matricula=matricula).first()

    if not maes1:
        flash("No se encontró el maestro.", "warning")
        return redirect(url_for('maestros.listado_maestros'))

    maes1.nombre = create_form.nombre.data
    maes1.apellidos = create_form.apellidos.data
    maes1.especialidad = create_form.especialidad.data
    maes1.email = create_form.email.data

    db.session.commit()
    flash("Maestro actualizado.", "success")
    return redirect(url_for('maestros.listado_maestros'))


@maestros.route('/maestros/eliminar', methods=['GET', 'POST'])
def eliminar_maestros():
    create_form = forms.MaestroForm(request.form)

    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maes1 = MaestrosModel.query.filter_by(matricula=matricula).first()

        if not maes1:
            flash("No se encontró el maestro.", "warning")
            return redirect(url_for('maestros.listado_maestros'))

        create_form.matricula.data = maes1.matricula
        create_form.nombre.data = maes1.nombre
        create_form.apellidos.data = maes1.apellidos
        create_form.especialidad.data = maes1.especialidad
        create_form.email.data = maes1.email

        return render_template('maestros/eliminarMaes.html', form=create_form)

    matricula = request.form.get('matricula') or create_form.matricula.data
    maes1 = MaestrosModel.query.filter_by(matricula=matricula).first()

    if maes1:
        db.session.delete(maes1)
        db.session.commit()
        flash("Maestro eliminado.", "success")
    else:
        flash("No se encontró el maestro.", "warning")

    return redirect(url_for('maestros.listado_maestros'))