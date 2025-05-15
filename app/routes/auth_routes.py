from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from app.controllers.user_controller import verificar_credenciales, obtener_usuario_por_id
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = 'tu_clave_secreta'

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get("email")
        contrasena = data.get("contrasena")

        usuario = verificar_credenciales(email, contrasena)
        print("Usuario autenticado:", usuario)  # ✅ Verificar el resultado

        if usuario:
            token = jwt.encode(
                {'user_id': usuario['id'], 'exp': datetime.utcnow() + timedelta(days=7)},
                SECRET_KEY,
                algorithm='HS256'
            )
            return jsonify({
                'token': token,
                'user': {
                    'id': usuario['id'],
                    'username': usuario['username'],
                    'email': usuario['email']
                }
            }), 200
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401
    except Exception as e:
        print("Error en login:", str(e))
        return jsonify({'error': 'Error interno del servidor'}), 500
    
@auth_bp.route('/auth/user', methods=['GET'])
def get_user_info():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token no proporcionado"}), 401

    try:
        token = token.replace("Bearer ", "")
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded.get('user_id')

        usuario = obtener_usuario_por_id(user_id)
        print("Usuario obtenido:", usuario)  # Verificar el resultado como diccionario

        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "El token ha expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500