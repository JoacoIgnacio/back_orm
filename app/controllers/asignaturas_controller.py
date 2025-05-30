from app.BD.conexion import obtener_conexion
import json
import shutil
import os
import traceback
import sys

def crear_asignaturas(asignaturas):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            print("🟡 Conexión abierta y cursor iniciado", file=sys.stderr)

            # Validación previa
            print("🔍 Datos recibidos para crear asignatura:", asignaturas, file=sys.stderr)

            # Convertir a JSON string para guardar en base de datos
            preguntas_json = json.dumps(asignaturas['preguntas'])
            respuestas_json = json.dumps(asignaturas['respuestas'])

            print("🟡 Ejecutando INSERT...", file=sys.stderr)
            sql = """
                INSERT INTO asignaturas (asignatura, alternativas, preguntas, respuestas, curso_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                asignaturas['asignatura'],
                asignaturas['alternativas'],
                preguntas_json,
                respuestas_json,
                asignaturas['curso_id']
            ))
            conexion.commit()
            print("✅ INSERT realizado correctamente", file=sys.stderr)

            # Obtener el ID recién creado
            id_asignatura = cursor.lastrowid

            # Consultar el registro para retornarlo
            sql_select = "SELECT * FROM asignaturas WHERE id = %s"
            cursor.execute(sql_select, (id_asignatura,))
            registro = cursor.fetchone()
            print("📄 Registro recuperado:", registro, file=sys.stderr)

    except Exception as err:
        print("❌ ERROR al crear la asignatura:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        registro = None

    finally:
        if conexion:
            conexion.close()
            print("🔒 Conexión cerrada", file=sys.stderr)

    if registro:
        return {
            "id": registro["id"],
            "asignatura": registro["asignatura"],
            "alternativas": registro["alternativas"],
            "preguntas": json.loads(registro["preguntas"]) if registro["preguntas"] else [],
            "respuestas": json.loads(registro["respuestas"]) if registro["respuestas"] else [],
            "curso_id": registro["curso_id"],
            "formato_imagen": registro["formato_imagen"],
            "total_columnas": registro["total_columnas"],
            "fecha_creacion": registro["fecha_creacion"],
            "fecha_actualizacion": registro["fecha_actualizacion"]
        }

    else:
        print("⚠️ No se pudo crear ni recuperar la asignatura", file=sys.stderr)
        return None

def actualizar_asignaturas(asignaturas_id, formato_imagen_base64, columnas):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "UPDATE asignaturas SET formato_imagen = %s, total_columnas = %s WHERE id = %s"
            cursor.execute(sql, (formato_imagen_base64, columnas, asignaturas_id))
            print("Actualizando asignatura con ID:", asignaturas_id)
            print("Longitud del formato base64:", len(formato_imagen_base64))

        conexion.commit()
    except Exception as err:
        import traceback
        print('ERROR al actualizar:', traceback.format_exc())
    finally:
        if conexion:
            conexion.close()

def obtener_asignaturas_por_curso(curso_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            query = """
                SELECT id, asignatura, alternativas, preguntas, respuestas, curso_id, total_columnas
                FROM asignaturas
                WHERE curso_id = %s
            """
            cursor.execute(query, (curso_id,))
            asignaturas = cursor.fetchall()
            print("Asignaturas obtenidas:", asignaturas)
            return asignaturas
    except Exception as e:
        print(f"Error al obtener asignaturas para el curso con ID {curso_id}:", e)
        return None
    finally:
        conexion.close()

def obtener_asignaturas():
    asignaturas = []
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM asignaturas"
            cursor.execute(sql)
            asignaturas = cursor.fetchall()
    except Exception as err:
        print('Error al obtener hojas de respuestas:', err)
    finally:
        if conexion:
            conexion.close()
    return asignaturas

def obtener_asignaturas_por_id(asignaturas_id):
    asignatura = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Conversión segura del ID a entero
            cursor.execute("SELECT * FROM asignaturas WHERE id = %s", (int(asignaturas_id),))
            registro = cursor.fetchone()

            if registro:
                asignatura = {
                    "id": registro["id"],
                    "asignatura": registro["asignatura"],
                    "alternativas": registro["alternativas"],
                    "preguntas": json.loads(registro["preguntas"]) if registro["preguntas"] else [],
                    "respuestas": json.loads(registro["respuestas"]) if registro["respuestas"] else [],
                    "curso_id": registro["curso_id"],
                    "formato_imagen": registro["formato_imagen"],
                    "total_columnas": registro["total_columnas"],
                    "fecha_creacion": registro["fecha_creacion"],
                    "fecha_actualizacion": registro["fecha_actualizacion"]
                }
            else:
                print(f"⚠️ No se encontró la asignatura con ID {asignaturas_id}")

    except Exception as err:
        import traceback
        print(f'❌ Error al obtener asignatura con ID {asignaturas_id}:\n', traceback.format_exc())
    finally:
        if conexion:
            conexion.close()

    return asignatura


def eliminar_asignatura(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT curso_id, asignatura FROM asignaturas WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                curso_id, nombre_asignatura = result
                cursor.execute("DELETE FROM asignaturas WHERE id = %s", (id,))
                conexion.commit()

                # Eliminar carpetas si aún existen por alguna razón
                ruta_formato = os.path.join("static", "formato", str(curso_id), nombre_asignatura)
                ruta_alumnos = os.path.join("static", "alumnos", str(curso_id), nombre_asignatura)
                for ruta in [ruta_formato, ruta_alumnos]:
                    if os.path.exists(ruta):
                        shutil.rmtree(ruta)
    finally:
        conexion.close()

def eliminar_asignatura_y_pruebas(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT curso_id, asignatura FROM asignaturas WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                curso_id, nombre_asignatura = result

                cursor.execute("DELETE FROM pruebas WHERE asignatura_id = %s", (id,))
                cursor.execute("DELETE FROM asignaturas WHERE id = %s", (id,))
                conexion.commit()

                ruta_formato = os.path.join("static", "formato", str(curso_id), nombre_asignatura)
                ruta_alumnos = os.path.join("static", "alumnos", str(curso_id), nombre_asignatura)
                for ruta in [ruta_formato, ruta_alumnos]:
                    if os.path.exists(ruta):
                        shutil.rmtree(ruta)

                return {"status": True, "mensaje": "Asignatura, pruebas y archivos eliminados correctamente"}
            else:
                return {"status": False, "mensaje": "La asignatura no existe"}
    except Exception as e:
        print("Error:", str(e))
        return {"status": False, "mensaje": "Error al eliminar la asignatura"}
    finally:
        conexion.close()
