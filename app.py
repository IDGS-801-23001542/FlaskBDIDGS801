from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db

from maestros import maestros as maestros_bp
from alumnos import alumnos as alumnos_bp
from cursos import cursos as cursos_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
csrf = CSRFProtect(app)

app.register_blueprint(maestros_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(cursos_bp)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)