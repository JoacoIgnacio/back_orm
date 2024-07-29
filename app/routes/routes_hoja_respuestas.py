from flask import Blueprint, request, jsonify
from app.controllers.hoja_respuestas_controller import (
    crear_hoja_respuestas,
    obtener_hoja_respuestas,
    obtener_hoja_respuestas_por_id,
    actualizar_hoja_respuestas,
    eliminar_hoja_respuestas,
    obtener_hojas_respuestas_por_usuario
)

hoja_respuestas_bp = Blueprint('hoja_respuestas', __name__)

# Ruta para crear una nueva hoja de respuestas
@hoja_respuestas_bp.route('/hojarespuestas', methods=['POST'])
def crear_nueva_hoja_respuestas():
    try:
        datos_hoja_respuestas = request.json
        hojas_respuestas = crear_hoja_respuestas(datos_hoja_respuestas)
        return jsonify({"status": True, "mensaje": "Hoja de respuestas creada exitosamente", 'hojas_respuestas': hojas_respuestas}), 201
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

# Ruta para obtener todas las hojas de respuestas
@hoja_respuestas_bp.route('/hojarespuestas', methods=['GET'])
def obtener_todas_las_hojas_respuestas():
    try:
        hojas_respuestas = obtener_hoja_respuestas()
        return jsonify(hojas_respuestas), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

@hoja_respuestas_bp.route('/hojasrespuestasporusuario/<int:usuario_id>', methods=['GET'])
def obtener_hojas_por_usuario(usuario_id):
    try:
        hojas_respuestas = obtener_hojas_respuestas_por_usuario(usuario_id)
        return jsonify({"status": True, "hojas_respuestas": hojas_respuestas}), 200
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500
   
# Ruta para obtener una hoja de respuestas por ID
@hoja_respuestas_bp.route('/hojarespuestas/<int:hoja_respuestas_id>', methods=['GET'])
def obtener_hoja_respuestas_por_id_route(hoja_respuestas_id):
    try:
        hoja_respuestas = obtener_hoja_respuestas_por_id(hoja_respuestas_id)
        if hoja_respuestas:
            return jsonify(hoja_respuestas), 200
        else:
            return jsonify({"mensaje": "Hoja de respuestas no encontrada"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para actualizar una hoja de respuestas por ID
@hoja_respuestas_bp.route('/hojarespuestas/<int:hoja_respuestas_id>', methods=['PUT'])
def actualizar_hoja_respuestas_por_id(hoja_respuestas_id):
    try:
        nuevos_datos = request.json
        actualizar_hoja_respuestas(hoja_respuestas_id, nuevos_datos)
        return jsonify({"mensaje": "Hoja de respuestas actualizada exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para eliminar una hoja de respuestas por ID
@hoja_respuestas_bp.route('/hojarespuestas/<int:hoja_respuestas_id>', methods=['DELETE'])
def eliminar_hoja_respuestas_por_id(hoja_respuestas_id):
    try:
        eliminar_hoja_respuestas(hoja_respuestas_id)
        return jsonify({"mensaje": "Hoja de respuestas eliminada exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
