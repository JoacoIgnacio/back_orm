from flask import Blueprint, request, jsonify
from app.controllers.asignaturas_controller import (
    crear_asignaturas,
    obtener_asignaturas,
    obtener_asignaturas_por_id,
    actualizar_asignaturas,
    eliminar_asignaturas,
    obtener_asignaturas_por_curso
)
from app.controllers.formato_controller import crear_formato
from app.controllers.cursos_controllers import obtener_curso_por_id

asignaturas_db_bp = Blueprint('asignaturas_db', __name__)

# Ruta para crear una nueva hoja de respuestas
@asignaturas_db_bp.route('/asignaturas', methods=['POST'])
def crear_asignaturas_route():
    try:
        datos_asignaturas = request.json
        asignatura = crear_asignaturas(datos_asignaturas)
        if asignatura :
            curso = obtener_curso_por_id(asignatura['curso_id'])
            formato = crear_formato(curso['curso'], asignatura['alternativas'], asignatura['asignatura'], len(datos_asignaturas['preguntas']))
            if formato :
                actualizar_asignaturas(asignatura['id'], formato['ruta'], formato['columnas'])
                return jsonify({"status": True, "mensaje": "Hoja de respuestas creada exitosamente", 'asignaturas': asignatura}), 201
            else :
                return jsonify({"status": False, "mensaje": "No se pudo crear el formato de la hoja de respuestas"}), 500
        else :
            return jsonify({"status": False, "mensaje": "No se pudo crear la Hoja de respuestas"}), 500
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

# Ruta para obtener todas las hojas de respuestas
@asignaturas_db_bp.route('/asignaturas', methods=['GET'])
def obtener_todas_las_asignaturas():
    try:
        asignaturas = obtener_asignaturas()
        return jsonify(asignaturas), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@asignaturas_db_bp.route('/asignaturasporcurso/<int:curso_id>', methods=['GET'])
def obtener_asignaturas_por_curso_route(curso_id):
    try:
        asignaturas = obtener_asignaturas_por_curso(curso_id)
        return jsonify({"status": True, "asignaturas": asignaturas}), 200
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500
    
   
# Ruta para obtener una hoja de respuestas por ID
@asignaturas_db_bp.route('/asignaturas/<int:asignaturas_id>', methods=['GET'])
def obtener_asignaturas_por_id_route(asignaturas_id):
    try:
        asignatura = obtener_asignaturas_por_id(asignaturas_id)
        if asignatura:
            return jsonify({"status": True,"mensaje": "Hoja de respuestas encontrada", "asignatura":asignatura}), 200
        else:
            return jsonify({"status": False,"mensaje": "Hoja de respuestas no encontrada"}), 404
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

# Ruta para actualizar una hoja de respuestas por ID
@asignaturas_db_bp.route('/asignaturas/<int:asignaturas_id>', methods=['PUT'])
def actualizar_asignaturas_por_id(asignaturas_id):
    try:
        ruta_formato = request.json.get('ruta_formato')
        actualizar_asignaturas(asignaturas_id, ruta_formato)
        return jsonify({"mensaje": "Hoja de respuestas actualizada exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para eliminar una hoja de respuestas por ID
@asignaturas_db_bp.route('/asignaturas/<int:asignaturas_id>', methods=['DELETE'])
def eliminar_asignaturas_por_id(asignaturas_id):
    try:
        eliminar_asignaturas(asignaturas_id)
        return jsonify({"mensaje": "Hoja de respuestas eliminada exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
