from . import cursos
from flask import render_template, request, redirect, url_for, flash
from models import db, Curso, Maestros, Alumnos, Inscripcion
from sqlalchemy.exc import IntegrityError

@cursos.route("/cursos", methods=["GET", "POST"])
@cursos.route("/cursos/listado", methods=["GET", "POST"])
def listado_cursos():
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        maestro_id = request.form.get("maestro_id")

        if not nombre or not maestro_id:
            flash("Complete los campos requeridos.", "warning")
            return redirect(url_for("cursos.listado_cursos"))

        cur = Curso(nombre=nombre, descripcion=descripcion, maestro_id=int(maestro_id))
        db.session.add(cur)
        db.session.commit()
        flash("Curso creado correctamente.", "success")
        return redirect(url_for("cursos.listado_cursos"))

    cursos_list = Curso.query.all()
    maestros = Maestros.query.all()
    return render_template("cursos/listadoCursos.html", cursos=cursos_list, maestros=maestros)


@cursos.route("/cursos/inscribir", methods=["GET", "POST"])
def inscribir_alumno():
    if request.method == "POST":
        curso_id = request.form.get("curso_id")
        alumno_id = request.form.get("alumno_id")

        if not curso_id or not alumno_id:
            flash("Seleccione curso y alumno.", "warning")
            return redirect(url_for("cursos.inscribir_alumno"))

        ins = Inscripcion(alumno_id=int(alumno_id), curso_id=int(curso_id))
        db.session.add(ins)
        try:
            db.session.commit()
            flash("Alumno inscrito correctamente.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Ese alumno ya está inscrito en ese curso.", "warning")

        return redirect(url_for("cursos.listado_cursos"))

    cursos_list = Curso.query.all()
    alumnos = Alumnos.query.all()
    return render_template("cursos/inscribir.html", cursos=cursos_list, alumnos=alumnos)


@cursos.route("/cursos/alumnos", methods=["GET"])
def alumnos_por_curso():
    curso_id = request.args.get("curso_id")
    curso = Curso.query.filter_by(id=curso_id).first()
    if not curso:
        flash("Curso no encontrado.", "warning")
        return redirect(url_for("cursos.listado_cursos"))

    maestro = curso.maestro
    alumnos = curso.alumnos
    return render_template("cursos/alumnosCurso.html", curso=curso, maestro=maestro, alumnos=alumnos)


@cursos.route("/cursos/eliminar", methods=["GET", "POST"])
def eliminar_curso():
    if request.method == "GET":
        curso_id = request.args.get("curso_id")
        curso = Curso.query.filter_by(id=curso_id).first()
        if not curso:
            flash("Curso no encontrado.", "warning")
            return redirect(url_for("cursos.listado_cursos"))

        return render_template("cursos/eliminarCurso.html", curso=curso)

    curso_id = request.form.get("curso_id")
    curso = Curso.query.filter_by(id=curso_id).first()
    if not curso:
        flash("Curso no encontrado.", "warning")
        return redirect(url_for("cursos.listado_cursos"))

    
    Inscripcion.query.filter_by(curso_id=curso.id).delete()
    db.session.delete(curso)
    db.session.commit()

    flash("Curso eliminado correctamente.", "danger")
    return redirect(url_for("cursos.listado_cursos"))


@cursos.route("/cursos/quitar_alumno", methods=["POST"])
def quitar_alumno():
    curso_id = request.form.get("curso_id")
    alumno_id = request.form.get("alumno_id")

    ins = Inscripcion.query.filter_by(curso_id=curso_id, alumno_id=alumno_id).first()
    if not ins:
        flash("Inscripción no encontrada.", "warning")
        return redirect(url_for("cursos.alumnos_por_curso") + f"?curso_id={curso_id}")

    db.session.delete(ins)
    db.session.commit()
    flash("Alumno removido del curso.", "danger")
    return redirect(url_for("cursos.alumnos_por_curso") + f"?curso_id={curso_id}")