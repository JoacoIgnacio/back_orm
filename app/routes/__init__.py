from flask import Blueprint

# ...

users_db_bp = Blueprint('usuarios_db', __name__)
asignaturas_db_bp = Blueprint('asignaturas_db', __name__)
pruebas_db_bp = Blueprint('pruebas_db', __name__)
alumnos_db_bp = Blueprint('alumnos_db', __name__)
cursos_db_bp = Blueprint('cursos_db', __name__)
scanner_db_bp = Blueprint('scanner_db', __name__)
formato_db_bp = Blueprint('formato_db', __name__)
auth_bp = Blueprint('auth', __name__)
