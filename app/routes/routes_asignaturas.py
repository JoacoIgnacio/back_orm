from flask import Blueprint, request, jsonify
from app.controllers.asignaturas_controller import (
    crear_asignaturas,
    obtener_asignaturas,
    obtener_asignaturas_por_id,
    actualizar_asignaturas,
    eliminar_asignatura,
    obtener_asignaturas_por_curso,
    eliminar_asignatura_y_pruebas
)
from app.controllers.formato_controller import crear_formato
from app.controllers.cursos_controllers import obtener_curso_por_id
import traceback
import sys

asignaturas_db_bp = Blueprint('asignaturas_db', __name__)

# Ruta para crear una nueva hoja de respuestas
@asignaturas_db_bp.route('/asignaturas', methods=['POST'])
def crear_asignaturas_route():
    try:
        datos_asignaturas = request.json
        asignatura = crear_asignaturas(datos_asignaturas)
        print("✅ asignatura recibida:", asignatura, file=sys.stderr)

        if asignatura is not None and 'curso_id' in asignatura:
            curso = obtener_curso_por_id(asignatura['curso_id'])
            print("📘 curso recibido:", curso, file=sys.stderr)

            formato = crear_formato(
                curso['curso'],
                asignatura['alternativas'],
                asignatura['asignatura'],
                len(asignatura['preguntas'])  # ✅ ya corregido
            )
            print("🖼️ formato generado:", "OK" if formato else "None", file=sys.stderr)

            if formato:
                actualizar_asignaturas(
                    asignatura['id'],
                    formato['formato_base64'],
                    formato['columnas']
                )
                return jsonify({
                    "status": True,
                    "mensaje": "Hoja de respuestas creada exitosamente",
                    "asignaturas": asignatura
                }), 201
            else:
                return jsonify({
                    "status": False,
                    "mensaje": "No se pudo generar el formato"
                }), 500
        else:
            return jsonify({
                "status": False,
                "mensaje": "No se pudo obtener la asignatura o curso"
            }), 500

    except Exception as err:
        import traceback
        print("❌ Error en POST /asignaturas:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({"status": False, "error": str(err)}), 500


# Ruta para obtener todas las hojas de respuestas
@asignaturas_db_bp.route('/asignaturas', methods=['GET'])
def obtener_todas_las_asignaturas():
    try:
        asignaturas = obtener_asignaturas()
        return jsonify(asignaturas), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para obtener asignaturas por curso
@asignaturas_db_bp.route('/asignaturasporcurso/<int:curso_id>', methods=['GET'])
def obtener_asignaturas_por_curso_route(curso_id):
    try:
        asignaturas = obtener_asignaturas_por_curso(curso_id)
        if not asignaturas:
            return jsonify({'status': False, 'mensaje': 'No hay asignaturas para este curso.'}), 200

        return jsonify({'status': True, 'asignaturas': asignaturas}), 200
    except Exception as e:
        return jsonify({'status': False, 'error': str(e)}), 500

# Ruta para obtener una hoja de respuestas por ID
@asignaturas_db_bp.route('/asignaturas/<int:asignaturas_id>', methods=['GET'])
def obtener_asignaturas_por_id_route(asignaturas_id):
    try:
        asignatura = obtener_asignaturas_por_id(asignaturas_id)
        if asignatura:
            return jsonify({
                "status": True,
                "mensaje": "Hoja de respuestas encontrada",
                "asignatura": asignatura
            }), 200
        else:
            return jsonify({
                "status": False,
                "mensaje": "Hoja de respuestas no encontrada"
            }), 404
    except Exception as err:
        return jsonify({"status": False, "error": str(err)}), 500

# Ruta para actualizar una hoja de respuestas (no es requerida con base64, pero se mantiene por compatibilidad)
@asignaturas_db_bp.route('/asignaturas/<int:asignaturas_id>', methods=['PUT'])
def actualizar_asignaturas_por_id(asignaturas_id):
    try:
        formato_imagen = request.json.get('formato_imagen')
        columnas = request.json.get('total_columnas')
        actualizar_asignaturas(asignaturas_id, formato_imagen, columnas)
        return jsonify({"mensaje": "Hoja de respuestas actualizada exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para eliminar una hoja de respuestas por ID
@asignaturas_db_bp.route('/asignaturas/<int:asignaturas_id>', methods=['DELETE'])
def eliminar_asignaturas_por_id(asignaturas_id):
    try:
        eliminar_asignatura(asignaturas_id)
        return jsonify({"mensaje": "Hoja de respuestas eliminada exitosamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# Ruta para eliminar asignatura + pruebas relacionadas
@asignaturas_db_bp.route('/asignaturas_completa/<int:id>', methods=['DELETE'])
def eliminar_asignatura_y_pruebas_route(id):
    resultado = eliminar_asignatura_y_pruebas(id)
    status_code = 200 if resultado["status"] else 404
    return jsonify(resultado), status_code
