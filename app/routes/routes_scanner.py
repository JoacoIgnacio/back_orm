import json
from flask import Blueprint, request, jsonify
from app.controllers.scanner_controller import (
    process_image,
    solve_test
)
from app.controllers.pruebas_controller import crear_prueba
from werkzeug.utils import secure_filename
import os

scanner_db_bp = Blueprint('scanner', __name__)

# Ruta para procesar la imagen
@scanner_db_bp.route('/scanner', methods=['POST'])
def scanner():
    try:
        alumno = json.loads(request.form.get('alumno'))
        alternativas = request.form.get('alternativas')
        answer_key = json.loads(request.form.get('ANSWER_KEY'))
        asignatura_id = request.form.get('id')
        total_columnas = request.form.get('total_columnas')
        result = obtener_imagen(request, alumno.get('id'))
        
        # Verificar si result contiene un error
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result)  # Retorna el error directamente

        # Procesar la imagen
        procesar_imagen = process_image(result, alumno.get('id'), total_columnas)  # Cambia esto según tu lógica de procesamiento

        if procesar_imagen:
            resolver_prueba = solve_test(answer_key, alternativas, alumno.get('id'))
            if isinstance(resolver_prueba, dict):
                nota = resolver_prueba.get('nota', 0.0)
                imagen_base64 = resolver_prueba.get('image')
                respuestas_alumno = json.dumps(resolver_prueba.get('respuestas_marcadas'))
            
                alumno_id = alumno.get('id')  # Asegúrate de obtener el ID correctamente
            
                prueba = {
                    'asignatura_id': asignatura_id, 
                    'alumno_id': alumno_id,
                    'respuestas': respuestas_alumno,
                    'nota': nota,
                    'activo': True  # Puedes ajustar esto según tus necesidades
                }
                
                crear_prueba(prueba)
                
                return jsonify({"status": True, "mensaje": "Se procesó la imagen", "nota": nota, "image": imagen_base64}), 201
            else:
                return jsonify({"status": False, "mensaje": "Error al resolver la prueba"}), 500
        else:
            return jsonify({"status": False, "mensaje": "No se pudo procesar la imagen"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

def procesar_texto(data_alumno):
    data_alumno_dict = {}
    try:
        for line in data_alumno.split('\n'):
            key, value = line.split(': ')
            data_alumno_dict[key.strip()] = value.strip()
    except ValueError:
        return jsonify({"error": "Formato de data_alumno no es válido"}), 400
    
    # Acceder a los valores dentro del diccionario
    nombre = data_alumno_dict.get('nombre', '')
    apellido = data_alumno_dict.get('apellido', '')
    id_curso = data_alumno_dict.get('id_curso', '')
    id_alumno = data_alumno_dict.get('id_alumno', '')

    return {
        'nombre': nombre,
        'apellido': apellido,
        'id_curso': id_curso,
        'id_alumno': id_alumno
    }
    
def obtener_imagen(request, alumno):
    try:
        # Verificar si la solicitud contiene archivos
        if 'image' not in request.files:
            return {"error": "No image file provided"}

        # Obtener el archivo de la solicitud
        file = request.files['image']

        if file.filename == '':
            return {"error": "No selected file"}

        # Asegurarse de que el archivo sea una imagen PNG
        if not file.filename.lower().endswith('.png'):
            return {"error": "Invalid file format. Only PNG files are allowed."}

        # Guardar el archivo en una ubicación temporal
        filename = f"{alumno}.png"
        filename = secure_filename(filename)
        file_path = os.path.join('static', filename)
        file.save(file_path)
        
        return file_path  # Devuelve la ruta del archivo guardado

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}