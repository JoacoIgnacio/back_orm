import json 
from flask import Blueprint, request, jsonify
from app.controllers.scanner_controller import procesar_y_evaluar_prueba
from app.controllers.pruebas_controller import crear_prueba
from werkzeug.utils import secure_filename
import os

scanner_db_bp = Blueprint('scanner', __name__)

@scanner_db_bp.route('/scanner', methods=['POST'])
def scanner():
    try:
        alumno = json.loads(request.form['alumno'])
        alternativas = int(request.form['alternativas'])
        answer_key = json.loads(request.form['ANSWER_KEY'])
        
        file = request.files.get('image')
        if not file:
            return jsonify({"status": False, "mensaje": "Imagen no proporcionada"}), 400

        filename = secure_filename(f"{alumno['id']}.png")
        ruta = os.path.join('static', filename)
        file.save(ruta)

        resultado = procesar_y_evaluar_prueba(ruta, alumno['id'], alternativas, answer_key)
        if resultado is None:
            return jsonify({"status": False, "mensaje": "Error al procesar la imagen"}), 500

        return jsonify({
            "status": True,
            "mensaje": "Se procesó correctamente",
            "correctas": resultado['respuestas_correctas'],
            "incorrectas": resultado['total_preguntas'] - resultado['respuestas_correctas'],
            "total_preguntas": resultado['total_preguntas'],
            "respuestas": resultado['respuestas_detectadas'],
            "image": resultado['imagen']
        }), 200
    except Exception as e:
        print(f'Error scanner route: {e}')
        return jsonify({"status": False, "mensaje": str(e)}), 500

@scanner_db_bp.route('/guardar-prueba', methods=['POST'])
def guardar_prueba():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": False, "mensaje": "No se enviaron datos"}), 400

        prueba = {
            'asignatura_id': data['asignatura_id'],
            'alumno_id': data['alumno_id'],
            'respuestas': json.dumps(data['respuestas']),
            'correctas': data['correctas'],
            'incorrectas': data['incorrectas'],
            'total_preguntas': data['total_preguntas'],
            'activo': True
        }
        crear_prueba(prueba)

        return jsonify({"status": True, "mensaje": "Prueba guardada exitosamente"}), 201
    except Exception as e:
        print(f'Error guardar_prueba route: {e}')
        return jsonify({"status": False, "mensaje": str(e)}), 500
