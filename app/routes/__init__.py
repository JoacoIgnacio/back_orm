from flask import Blueprint

# ...

users_db_bp = Blueprint('users_db', __name__)
hoja_respuestas_bp = Blueprint('hoja_respuestas', __name__)
pruebas_db_bp = Blueprint('pruebas_db', __name__)
alumnos_db_bp = Blueprint('alumnos_db', __name__)
cursos_db_bp = Blueprint('cursos_db', __name__)
scanner_db_bp = Blueprint('scanner_db', __name__)
generador_qr_bp = Blueprint('generador_qr', __name__)
