# app/routes/routes_cursos.py
from flask import Blueprint, request, jsonify
from app.controllers.cursos_controllers import (
    crear_curso,
    obtener_cursos_por_usuario,
    obtener_curso_por_id,
    actualizar_curso,
    eliminar_curso,
)

cursos_db_bp = Blueprint('cursos_db', __name__)

# Ruta para crear un nuevo curso asociado a un usuario
@cursos_db_bp.route('/cursos', methods=['POST'])
def crear_nuevo_curso():
    try:
        datos_curso = request.json
        user_id = datos_curso.get('user_id')

        if not user_id:
            return jsonify({"status": False, "error": "El ID del usuario es requerido"}), 400

        curso_id = crear_curso(datos_curso)
        return jsonify({"status": True, "mensaje": "Curso creado exitosamente", 'curso_id': curso_id}), 201
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

# Ruta para obtener todos los cursos de un usuario por ID en la URL
@cursos_db_bp.route('/cursos/user_id/<int:user_id>', methods=['GET'])
def obtener_cursos_por_usuario_id(user_id):
    try:
        cursos = obtener_cursos_por_usuario(user_id)
        return jsonify({"status": True, "cursos": cursos}), 200
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500
    
# Ruta para eliminar todos los cursos de un usuario (si es lo que deseas)
@cursos_db_bp.route('/cursos/user_id/<int:user_id>', methods=['DELETE'])
def eliminar_cursos_por_usuario(user_id):
    try:
        cursos = obtener_cursos_por_usuario(user_id)
        if not cursos:
            return jsonify({"status": False, "error": "El usuario no tiene cursos"}), 404
        
        for curso in cursos:
            eliminar_curso(curso["id"])

        return jsonify({"status": True, "mensaje": "Todos los cursos del usuario fueron eliminados"}), 200
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500
    
# Ruta para obtener un curso por su ID
@cursos_db_bp.route('/cursos/<int:curso_id>', methods=['GET'])
def obtener_curso(curso_id):
    try:
        curso = obtener_curso_por_id(curso_id)
        if curso:
            return jsonify({"status": True, "curso": curso}), 200
        else:
            return jsonify({"status": False, 'error': "Curso no encontrado"}), 404
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

# Ruta para actualizar un curso por ID
@cursos_db_bp.route('/cursos/<int:curso_id>', methods=['PUT'])
def actualizar_curso_por_id(curso_id):
    try:
        nuevos_datos = request.json
        actualizar_curso(curso_id, nuevos_datos)
        return jsonify({"status": True, "mensaje": "Curso actualizado exitosamente"}), 200
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

# Ruta para eliminar un curso por ID
@cursos_db_bp.route('/cursos/<int:curso_id>', methods=['DELETE'])
def eliminar_curso_por_id(curso_id):
    try:
        eliminado, alumnos_eliminados = eliminar_curso(curso_id)
        if eliminado:
            return jsonify({
                "status": True,
                "mensaje": f"Curso eliminado exitosamente. Alumnos eliminados: {alumnos_eliminados}"
            }), 200
        else:
            return jsonify({"status": False, "error": "Curso no encontrado"}), 404
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

