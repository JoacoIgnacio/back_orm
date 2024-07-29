# app/DB/routes/cursos_routes.py
from flask import Blueprint, request, jsonify
from app.controllers.cursos_controllers import (
    crear_curso,
    obtener_cursos,
    obtener_curso_por_id,
    actualizar_curso,
    eliminar_curso,
    obtener_cursos_por_usuario
)

cursos_db_bp = Blueprint('cursos_db', __name__)

# Ruta para crear un nuevo curso
@cursos_db_bp.route('/cursos', methods=['POST'])
def crear_nuevo_curso():
    try:
        datos_curso = request.json
        id_curso = crear_curso(datos_curso)
        return jsonify({"status": True, "mensaje": "Curso creado exitosamente", 'id_curso': id_curso}), 201
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

# Ruta para obtener todos los cursos
@cursos_db_bp.route('/cursos', methods=['GET'])
def obtener_todos_los_cursos():
    try:
        cursos = obtener_cursos()
        return jsonify(cursos), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@cursos_db_bp.route('/cursosporusuario/<int:user_id>', methods=['GET'])
def obtener_cursos_por_usuario_id(user_id):
    try:
        cursos = obtener_cursos_por_usuario(user_id)
        return jsonify({"status": True, "cursos": cursos})
    except Exception as err:
        return jsonify({"status": False, 'error': str(err)}), 500

@cursos_db_bp.route('/cursos/<int:curso_id>', methods=['GET'])
def obtener_curso(curso_id):
    try:
        curso = obtener_curso_por_id(curso_id)
        if curso:
            return jsonify({"status": True, "curso": curso})
        else:
            return jsonify({"status": False, 'error': "Curso no encontrado"}), 404
    except Exception as err:
        print(f'Error en el endpoint: {err}')  # Depuración: imprimir error detallado
        return jsonify({"status": False, "error": str(err)}), 500


# Ruta para actualizar un curso por ID
@cursos_db_bp.route('/cursos/<int:curso_id>', methods=['PUT'])
def actualizar_curso_por_id(curso_id):
    try:
        nuevos_datos = request.json
        actualizar_curso(curso_id, nuevos_datos)
        return jsonify({"mensaje": "Curso actualizado exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para eliminar un curso por ID
@cursos_db_bp.route('/cursos/<int:curso_id>', methods=['DELETE'])
def eliminar_curso_por_id(curso_id):
    try:
        eliminar_curso(curso_id)
        return jsonify({"mensaje": "Curso eliminado exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
