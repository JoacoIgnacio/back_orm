from flask import Blueprint, request, jsonify
from app.controllers.user_controller import crear_usuario, obtener_usuarios, obtener_usuario_por_id, actualizar_usuario, eliminar_usuario

users_db_bp = Blueprint('users_db', __name__)

@users_db_bp.route('/users', methods=['POST'])
def crear_nuevo_usuario():
    try:
        datos_usuario = request.json
        crear_usuario(datos_usuario)
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para obtener todos los usuarios
@users_db_bp.route('/users', methods=['GET'])
def obtener_todos_los_usuarios():
    try:
        usuarios = obtener_usuarios()
        return jsonify(usuarios), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para obtener un usuario por ID
@users_db_bp.route('/users/<int:user_id>', methods=['GET'])
def obtener_usuario_por_id_route(user_id):
    try:
        usuario = obtener_usuario_por_id(user_id)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para actualizar un usuario por ID
@users_db_bp.route('/users/<int:user_id>', methods=['PUT'])
def actualizar_usuario_por_id(user_id):
    try:
        nuevos_datos = request.json
        actualizar_usuario(user_id, nuevos_datos)
        return jsonify({"mensaje": "Usuario actualizado exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para eliminar un usuario por ID
@users_db_bp.route('/users/<int:user_id>', methods=['DELETE'])
def eliminar_usuario_por_id(user_id):
    try:
        eliminar_usuario(user_id)
        return jsonify({"mensaje": "Usuario eliminado exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500