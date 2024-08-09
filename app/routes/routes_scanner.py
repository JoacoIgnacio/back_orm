import json
from flask import Blueprint, request, jsonify
from app.controllers.scanner_controller import (
    process_image,
    solve_test
)
from app.controllers.respuestas_alumnos_controller import agregar_respuestas_alumnos
from app.controllers.pruebas_controller import crear_prueba
import json

scanner_db_bp = Blueprint('scanner', __name__)

# Ruta para procesar la imagen
@scanner_db_bp.route('/scanner', methods=['POST'])
def scanner():
    try:
        request_data = request.get_json()
        procesar_imagen = process_image(request_data['image'], request_data['alternativas'])
        if procesar_imagen:
            resolver_prueba = solve_test(request_data['ANSWER_KEY'], request_data['alternativas'])
            nota = resolver_prueba.get('nota', 0.0)
            imagen = resolver_prueba.get('image')
            respuestas_alumno = json.dumps(resolver_prueba.get('respuestas_marcadas'))
            
            data_alumno = request_data['data_alumno']
            asignatura_id = request_data['id']
        
            alumno_id = data_alumno[0]
            
            prueba = {
                'asignatura_id': asignatura_id, 
                'alumno_id': alumno_id,
                'respuestas': respuestas_alumno,
                'nota': nota,
                'activo': True  # Puedes ajustar esto según tus necesidades
            }
                
            
            crear_prueba(prueba)
            
            return jsonify({"status": True, "mensaje": "Se procesó la imagen", "nota": nota, "image": imagen}), 201
        else:
            return jsonify({"status": False, "mensaje": "No se pudo procesar la imagen"}), 500
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

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