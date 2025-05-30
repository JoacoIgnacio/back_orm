from flask import Flask
from flask_cors import CORS  # Importa la extensión CORS
from app.routes.routes_users import users_db_bp 
from app.routes.routes_asignaturas import asignaturas_db_bp
from app.routes.routes_pruebas import pruebas_db_bp
from app.routes.routes_alumnos import alumnos_db_bp
from app.routes.routes_cursos import cursos_db_bp
from app.routes.routes_scanner import scanner_db_bp
from app.routes.routes_formato import formato_db_bp
from app.routes.auth_routes import auth_bp
app = Flask(__name__)

# Configuración de la aplicación, si es necesario
# app.config['DEBUG'] = True

# Registra la blueprint de la API
app.register_blueprint(users_db_bp)
app.register_blueprint(asignaturas_db_bp)
app.register_blueprint(pruebas_db_bp)
app.register_blueprint(alumnos_db_bp)
app.register_blueprint(cursos_db_bp)
app.register_blueprint(scanner_db_bp)
app.register_blueprint(formato_db_bp)
app.register_blueprint(auth_bp)


# Configuración de CORS
CORS(app)  # Esto permite solicitudes desde cualquier origen

@app.route("/")
def home():
    return "✅ Backend Flask desplegado correctamente en Render"
