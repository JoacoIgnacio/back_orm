# app/DB/routes/alumnos_routes.py
from flask import Blueprint, request, jsonify
from app.controllers.alumnos_controller import (
    crear_alumno,
    obtener_alumnos,
    obtener_alumno_por_id,
    actualizar_alumno,
    eliminar_alumno,
    obtener_alumnos_por_curso,
    eliminar_alumnos_por_curso
)

alumnos_db_bp = Blueprint('alumnos_db', __name__)

# Ruta para crear un nuevo alumno
@alumnos_db_bp.route('/alumnos', methods=['POST'])
def crear_nuevo_alumno():
    try:
        datos_alumno = request.json
        alumno = crear_alumno(datos_alumno)
        return jsonify({"status": True, "mensaje": "Alumno creado exitosamente", 'alumno': alumno}), 201
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

# Ruta para obtener todos los alumnos
@alumnos_db_bp.route('/alumnos', methods=['GET'])
def obtener_todos_los_alumnos():
    try:
        alumnos = obtener_alumnos()
        return jsonify(alumnos), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@alumnos_db_bp.route('/alumnos/curso/<int:curso_id>', methods=['GET'])
def obtener_alumnos_por_curso_route(curso_id):
    try:
        alumnos = obtener_alumnos_por_curso(curso_id)
        return jsonify(alumnos), 200
    except Exception as err:
        print(f'Error en obtener_alumnos_por_curso_route: {err}')
        return jsonify({"error": str(err)}), 500
    
# Ruta para obtener un alumno por ID
@alumnos_db_bp.route('/alumnos/<int:alumno_id>', methods=['GET'])
def obtener_alumno_por_id_route(alumno_id):
    try:
        alumno = obtener_alumno_por_id(alumno_id)
        if alumno:
            return jsonify(alumno), 200
        else:
            return jsonify({"mensaje": "Alumno no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para actualizar un alumno por ID
@alumnos_db_bp.route('/alumnos/<int:alumno_id>', methods=['PUT'])
def actualizar_alumno_por_id(alumno_id):
    try:
        nuevos_datos = request.json
        actualizar_alumno(alumno_id, nuevos_datos)
        return jsonify({"mensaje": "Alumno actualizado exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para eliminar un alumno por ID
@alumnos_db_bp.route('/alumnos/<int:alumno_id>', methods=['DELETE'])
def eliminar_alumno_por_id(alumno_id):
    try:
        eliminar_alumno(alumno_id)
        return jsonify({"mensaje": "Alumno eliminado exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
 

@alumnos_db_bp.route('/eliminaralumnosporcurso/<int:curso_id>', methods=['DELETE'])
def eliminar_alumnos_por_curso_endpoint(curso_id):
    try:
        eliminar_alumnos_por_curso(curso_id)
        return jsonify({"message": "Alumnos eliminados correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
