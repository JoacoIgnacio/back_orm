from flask import Blueprint, request, jsonify
from app.controllers.pruebas_controller import crear_prueba, obtener_pruebas, obtener_prueba_por_id, actualizar_prueba, eliminar_prueba, obtener_notas_por_asignatura_controller

pruebas_db_bp = Blueprint('pruebas_db', __name__)

# Ruta para crear una nueva prueba
@pruebas_db_bp.route('/pruebas', methods=['POST'])
def crear_nueva_prueba():
    try:
        datos_prueba = request.json
        crear_prueba(datos_prueba)
        return jsonify({"mensaje": "Prueba creada exitosamente"}), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para obtener todas las pruebas
@pruebas_db_bp.route('/pruebas', methods=['GET'])
def obtener_todas_las_pruebas():
    try:
        pruebas = obtener_pruebas()
        return jsonify(pruebas), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para obtener una prueba por ID
@pruebas_db_bp.route('/pruebas/<int:prueba_id>', methods=['GET'])
def obtener_prueba_por_id_route(prueba_id):
    try:
        pruebas = obtener_prueba_por_id(prueba_id)
        if pruebas:
            return jsonify({"status": True, "pruebas": pruebas}), 200
        else:
            return jsonify({"status": False, "mensaje": "Prueba no encontrada"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para actualizar una prueba por ID
@pruebas_db_bp.route('/pruebas/<int:prueba_id>', methods=['PUT'])
def actualizar_prueba_por_id(prueba_id):
    try:
        nuevos_datos = request.json
        actualizar_prueba(prueba_id, nuevos_datos)
        return jsonify({"mensaje": "Prueba actualizada exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para eliminar una prueba por ID
@pruebas_db_bp.route('/pruebas/<int:prueba_id>', methods=['DELETE'])
def eliminar_prueba_por_id(prueba_id):
    try:
        eliminar_prueba(prueba_id)
        return jsonify({"mensaje": "Prueba eliminada exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
@pruebas_db_bp.route('/pruebas/notas_por_asignatura/<int:asignatura_id>', methods=['GET'])
def obtener_notas_por_asignatura_route(asignatura_id):
    notas = obtener_notas_por_asignatura_controller(asignatura_id)
    if notas is not None:
        return jsonify(notas)
    else:
        return jsonify({"error": "Error interno al obtener notas"}), 500