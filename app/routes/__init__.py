from flask import Blueprint

# ...

users_db_bp = Blueprint('usuarios_db', __name__, url_prefix='/users')
asignaturas_db_bp = Blueprint('alumnos_db', __name__, url_prefix='/alumnos')
pruebas_db_bp = Blueprint('asignaturas_db', __name__, url_prefix='/asignaturas')
alumnos_db_bp = Blueprint('cursos_db', __name__, url_prefix='/cursos')
cursos_db_bp = Blueprint('formato_db', __name__, url_prefix='/formato')
scanner_db_bp = Blueprint('scanner_db', __name__, url_prefix='/scanner')
formato_db_bp = Blueprint('pruebas_db', __name__, url_prefix='/pruebas')
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
