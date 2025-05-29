from flask import Blueprint, request, jsonify
from app.controllers.scanner_controller import procesar_y_evaluar_prueba
from app.controllers.pruebas_controller import crear_prueba
from app.controllers.asignaturas_controller import obtener_asignaturas_por_id
import json
import base64
import cv2
import numpy as np
from PIL import Image
import io

scanner_db_bp = Blueprint('scanner', __name__)

@scanner_db_bp.route('/scanner', methods=['POST'])
def scanner():
    try:
        # Extraer y convertir datos del formulario
        alumno = json.loads(request.form['alumno'])
        alternativas = int(request.form['alternativas'])
        answer_key = json.loads(request.form['ANSWER_KEY'])
        asignatura_id = int(request.form['id'])
        columnas = int(request.form['total_columnas'])

        # Leer imagen cargada
        file = request.files.get('image')
        if not file:
            return jsonify({"status": False, "mensaje": "Imagen no proporcionada"}), 400

        imagen_pil = Image.open(file.stream).convert('RGB')
        imagen = cv2.cvtColor(np.array(imagen_pil), cv2.COLOR_RGB2BGR)

        # Obtener formato desde la base de datos
        asignatura = obtener_asignaturas_por_id(asignatura_id)
        if not asignatura or not asignatura.get('formato_imagen'):
            return jsonify({"status": False, "mensaje": "Formato no encontrado"}), 404

        formato_bytes = base64.b64decode(asignatura['formato_imagen'])
        formato_pil = Image.open(io.BytesIO(formato_bytes)).convert('RGB')
        formato_cv = cv2.cvtColor(np.array(formato_pil), cv2.COLOR_RGB2BGR)

        # Procesar imagen con OpenCV
        resultado = procesar_y_evaluar_prueba(
            imagen, formato_cv, alumno, alternativas, answer_key, columnas
        )

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
