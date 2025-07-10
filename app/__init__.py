from flask import Flask
from flask_cors import CORS

# Importa los blueprints definidos en sus propios archivos de rutas
from app.routes.routes_users import users_db_bp
from app.routes.routes_asignaturas import asignaturas_db_bp
from app.routes.routes_pruebas import pruebas_db_bp
from app.routes.routes_alumnos import alumnos_db_bp
from app.routes.routes_cursos import cursos_db_bp
from app.routes.routes_scanner import scanner_db_bp
from app.routes.routes_formato import formato_db_bp
from app.routes.auth_routes import auth_bp

app = Flask(__name__)

# Registra todos los blueprints bajo el prefijo común /back_orm
app.register_blueprint(users_db_bp, url_prefix='/back_orm')
app.register_blueprint(asignaturas_db_bp, url_prefix='/back_orm')
app.register_blueprint(pruebas_db_bp, url_prefix='/back_orm')
app.register_blueprint(alumnos_db_bp, url_prefix='/back_orm')
app.register_blueprint(cursos_db_bp, url_prefix='/back_orm')
app.register_blueprint(scanner_db_bp, url_prefix='/back_orm')
app.register_blueprint(formato_db_bp, url_prefix='/back_orm')
app.register_blueprint(auth_bp, url_prefix='/back_orm')

# Habilita CORS para frontend móvil
CORS(app)
