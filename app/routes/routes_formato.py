import csv
import datetime
from flask import Blueprint, Response, jsonify, send_from_directory, send_file
import os
import zipfile
from io import StringIO
from app.controllers.alumnos_controller import obtener_alumnos_por_curso
from app.controllers.formato_controller import agregar_qr_alumno
from app.controllers.cursos_controllers import obtener_curso_por_nombre
from app.controllers.asignaturas_controller import obtener_asignaturas_por_nombre
from app.controllers.pruebas_controller import obtener_prueba_por_id

from io import BytesIO

formato_db_bp = Blueprint('formato', __name__)
    
@formato_db_bp.route('/formato/<curso>/<asignatura>', methods=['GET'])
def obtener_imagen_formato_route(curso, asignatura, filename):
    try:
        # Define la carpeta donde se encuentran las imágenes
        image_directory = os.path.join(os.getcwd(), f'static/formato/{curso}/{asignatura}')
        # Verifica si el archivo existe en el directorio
        if os.path.exists(os.path.join(image_directory, filename)):
            # Sirve la imagen desde el directorio especificado
            return send_from_directory(image_directory, filename)
        else:
            raise FileNotFoundError("Archivo no encontrado")
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 404
    
@formato_db_bp.route('/alumnos/<curso>/<asignatura>/descargarFormatos', methods=['GET'])
def descargar_imagenes_alumnos_route(curso, asignatura):
    try:
        # Define la carpeta donde se encuentran las imágenes
        image_directory = os.path.join(os.getcwd(), f'static/alumnos/{curso}/{asignatura}')

        # Verifica si el directorio existe
        if not os.path.exists(image_directory):
            raise FileNotFoundError("Directorio no encontrado")

        # Crear un archivo ZIP en memoria
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            # Recorrer todos los archivos en el directorio
            for foldername, subfolders, filenames in os.walk(image_directory):
                for filename in filenames:
                    # Ruta completa del archivo
                    file_path = os.path.join(foldername, filename)
                    # Agregar el archivo al ZIP
                    zf.write(file_path, os.path.relpath(file_path, image_directory))
        
        memory_file.seek(0)

        # Enviar el archivo ZIP al cliente
        return send_file(
            memory_file,
            as_attachment=True,
            download_name=f'{curso}_{asignatura}_imagenes.zip',
            mimetype='application/zip'
        )
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 404
    
@formato_db_bp.route('/formato/<curso>/<asignatura>/generarFormatos', methods=['GET'])
def generar_formato_alumnos_route(curso, asignatura):
    try:
        resultados = []
        curso = obtener_curso_por_nombre(curso)
        if not curso:
            return jsonify({"status": False, "mensaje": "No se encontró ningún curso"}), 404

        asignatura = obtener_asignaturas_por_nombre(asignatura)
        if not asignatura:
            return jsonify({"status": False, "mensaje": "No se encontró ninguna asignatura"}), 404

        alumnos = obtener_alumnos_por_curso(curso['id'])
        if not alumnos:
            return jsonify({"status": False, "mensaje": "No se encontró ningún alumno en el curso"}), 404

        for alumno in alumnos:
            data_alumnos = {
                'id': alumno[0],
                'nombre': alumno[1],
                'apellido': alumno[2],
                'curso_id': alumno[3],
                'asignatura': asignatura['id']
            }
            resultados.append(data_alumnos)

        result_qr_alumnos = agregar_qr_alumno(resultados, curso['curso'], asignatura['asignatura'], asignatura['ruta_formato'])
        if not result_qr_alumnos:
            return jsonify({"status": False, "mensaje": "No se pudo crear la hoja de respuestas"}), 500

        return jsonify({"status": True, "mensaje": "Hoja de respuestas creada exitosamente", "imagenes": result_qr_alumnos}), 201

    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

@formato_db_bp.route('/alumnos/<curso>/<asignatura>/descargarCSV', methods=['GET'])
def download_alumnos(curso, asignatura):
    try:
        print('Iniciando proceso de obtención de pruebas...')
        
        asignatura = obtener_asignaturas_por_nombre(asignatura)
        if asignatura:
            alumnos = obtener_prueba_por_id(asignatura['id'])
            if alumnos:
                # Obtener la fecha actual
                today = datetime.datetime.now()
                formatted_date = today.strftime('%Y%m%d')

                # Nombre del archivo
                file_name = f"{curso}_{asignatura['asignatura']}_{formatted_date}.csv"

                # Generar el contenido CSV usando StringIO
                output = StringIO()
                writer = csv.writer(output)
                writer.writerow(['Nombre', 'Nota', 'Respuesta'])  # Header

                for row in alumnos:
                    writer.writerow([row['nombre'], row['nota'], row['respuesta']])

                # Mover el puntero del buffer al inicio
                output.seek(0)

                # Crear la respuesta como un archivo CSV
                response = Response(output.getvalue(), mimetype='text/csv')
                response.headers.set("Content-Disposition", "attachment", filename=file_name)
                return response
            else:
                return jsonify({"status": False, "mensaje": "No se encontraron alumnos"}), 500
        else:
            return jsonify({"status": False, "mensaje": "No se encontro ningun asignatura"}), 500    
    except Exception as e:
        print(f"Error al guardar el archivo CSV: {e}")
        # Aquí puedes usar alguna librería para mostrar alertas si es necesario.
