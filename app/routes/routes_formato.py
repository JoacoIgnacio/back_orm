from flask import Blueprint, Response, jsonify, send_file
import os
import zipfile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import qrcode
import json
import base64

from app.controllers.alumnos_controller import obtener_alumnos_por_curso
from app.controllers.formato_controller import agregar_qr_alumno
from app.controllers.cursos_controllers import obtener_curso_por_id
from app.controllers.asignaturas_controller import obtener_asignaturas_por_id

formato_db_bp = Blueprint('formato', __name__)

@formato_db_bp.route('/alumnos/<curso>/<asignatura>/descargarFormatos', methods=['GET'])
def descargar_imagenes_alumnos_route(curso, asignatura):
    try:
        curso_obj = obtener_curso_por_id(curso)
        asignatura_obj = obtener_asignaturas_por_id(asignatura)

        if not curso_obj or not asignatura_obj:
            raise FileNotFoundError("Curso o asignatura no válidos")

        alumnos = obtener_alumnos_por_curso(curso)
        if not alumnos:
            raise Exception("No se encontraron alumnos para este curso.")

        # Obtener imagen base64 desde la base de datos
        formato_base64 = asignatura_obj.get('formato_imagen')
        if not formato_base64:
            raise Exception("Formato de imagen no encontrado.")

        # Decodificar base64 a imagen PIL
        
        formato_bytes = base64.b64decode(formato_base64)
        imagen_base = Image.open(BytesIO(formato_bytes)).convert("RGBA")

        # Crear archivo ZIP en memoria
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for alumno in alumnos:
                imagen = imagen_base.copy()
                dibujar = ImageDraw.Draw(imagen)

                # Generar QR personalizado
                qr_data = {
                    "id": alumno["id"],
                    "nombre": alumno["nombre"],
                    "apellido": alumno["apellido"],
                    "curso_id": curso,
                    "asignatura_id": asignatura
                }
                qr_info = json.dumps(qr_data)
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_info)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

                # Redimensionar QR
                qr_size = 250
                qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
                qr_x = imagen.width - qr_size - 50
                qr_y = 50
                imagen.paste(qr_img, (qr_x, qr_y))

                # Fuente (igual que en tu función original)
                try:
                    font_path = os.path.join(os.getcwd(), "fonts", "Lato-Regular.ttf")
                    fuente_labels = ImageFont.truetype(font_path, 20)
                except:
                    fuente_labels = ImageFont.load_default()

                # Posiciones exactas como en la versión previa
                dibujar.text((140, 100), alumno['nombre'], fill="black", font=fuente_labels)
                dibujar.text((140, 180), alumno['apellido'], fill="black", font=fuente_labels)

                # Guardar imagen en memoria dentro del ZIP
                img_io = BytesIO()
                imagen = imagen.convert("RGBA").resize((1272, 1647))
                imagen.save(img_io, format='PNG')
                img_io.seek(0)
                nombre_archivo = f"{alumno['nombre']}_{alumno['apellido']}.png"
                zf.writestr(nombre_archivo, img_io.getvalue())


        memory_file.seek(0)
        return send_file(
            memory_file,
            as_attachment=True,
            download_name=f"Formatos_{curso_obj['curso']}_{asignatura_obj['asignatura']}.zip",
            mimetype='application/zip'
        )

    except Exception as err:
        import traceback
        print("❌ Error al generar formatos:", traceback.format_exc())
        return jsonify({"status": False, "error": str(err)}), 404

@formato_db_bp.route('/formato_general/<int:curso_id>/<int:asignatura_id>', methods=['GET'])
def descargar_formato_general(curso_id, asignatura_id):
    try:
        curso = obtener_curso_por_id(curso_id)
        asignatura = obtener_asignaturas_por_id(asignatura_id)

        if not curso or not asignatura:
            return jsonify({"status": False, "mensaje": "Curso o asignatura no encontrados"}), 404

        # Cargar la imagen base desde la base de datos
        formato_base64 = asignatura['formato_imagen']
        formato_bytes = base64.b64decode(formato_base64)
        imagen = Image.open(BytesIO(formato_bytes)).convert('RGBA')

        draw = ImageDraw.Draw(imagen)

        # Crear QR solo con curso_id y asignatura_id
        qr_data = {
            "curso_id": curso_id,
            "asignatura_id": asignatura_id
        }
        qr = qrcode.make(json.dumps(qr_data))
        qr = qr.resize((150, 150))
        imagen.paste(qr, (imagen.width - 180, 30))

        # Preparar imagen para respuesta
        img_io = BytesIO()
        imagen.save(img_io, format='PNG')
        img_io.seek(0)

        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'formato_general_{curso["curso"]}_{asignatura["asignatura"]}.png'
        )
    except Exception as err:
        import traceback
        print("❌ Error en formato_general:", traceback.format_exc())
        return jsonify({"status": False, "error": str(err)}), 500