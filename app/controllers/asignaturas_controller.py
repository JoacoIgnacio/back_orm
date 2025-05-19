from app.BD.conexion import obtener_conexion
import json
from typing import List, Dict
import shutil
import os
import base64

def crear_asignaturas(asignaturas):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Convertir la lista de preguntas y respuestas a una cadena JSON
            preguntas_json = json.dumps(asignaturas['preguntas'])
            respuestas_json = json.dumps(asignaturas['respuestas'])

            # Insertar nueva hoja de respuestas
            sql = "INSERT INTO asignaturas (asignatura, alternativas, preguntas, respuestas, curso_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (asignaturas['asignatura'], asignaturas['alternativas'], preguntas_json, respuestas_json, asignaturas['curso_id']))
            conexion.commit()

            # Obtener el ID del registro insertado
            id_asignatura = cursor.lastrowid

            # Consultar el registro completo recién insertado
            sql_select = "SELECT * FROM asignaturas WHERE id = %s"
            cursor.execute(sql_select, (id_asignatura,))
            registro = cursor.fetchone()

        print('Hoja de respuestas creada exitosamente')
    except Exception as err:
        print('Error al crear hoja de respuestas:', err)
        registro = None
    finally:
        if conexion:
            conexion.close()
    return {"id": registro[0], "asignatura": registro[1], "alternativas": registro[2], "preguntas": registro[3], "respuestas": registro[4], "curso_id": registro[5]}


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
            sql = "SELECT * FROM asignaturas WHERE id = %s"
            cursor.execute(sql, (asignaturas_id,))
            asignatura = cursor.fetchone()
            
            # Verificar si se obtuvo un resultado antes de acceder a los índices
            if not asignatura:
                print(f"Error: No se encontró la asignatura con ID {asignaturas_id}")
                return None

            # Verificar la cantidad de columnas antes de acceder a ellas
            asignatura_dict = {
                "id": asignatura[0],
                "asignatura": asignatura[1],
                "alternativas": asignatura[2],
                "preguntas": json.loads(asignatura[3]) if asignatura[3] else [],
                "respuestas": json.loads(asignatura[4]) if asignatura[4] else [],
                "curso_id": asignatura[5],
                "ruta_formato": asignatura[6] if len(asignatura) > 6 else None,
                "total_columnas": asignatura[7] if len(asignatura) > 7 else None
            }

    except Exception as err:
        print(f'Error al obtener hoja de respuestas con ID {asignaturas_id}:', err)
        return None  # Evita devolver datos corruptos

    finally:
        if conexion:
            conexion.close()

    return asignatura_dict

def actualizar_asignaturas(asignaturas_id, ruta_formato, columnas):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "UPDATE asignaturas SET ruta_formato = %s, total_columnas = %s WHERE id = %s"
            cursor.execute(sql, (ruta_formato, columnas, asignaturas_id))
        conexion.commit()
    except Exception as err:
        print(f'Error al actualizar hoja de respuestas con ID {asignaturas_id}:', err)
    finally:
        if conexion:
            conexion.close()

def eliminar_asignatura(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Obtener curso_id y nombre antes de eliminar
            cursor.execute("SELECT curso_id, nombre FROM asignaturas WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                curso_id, nombre_asignatura = result

                cursor.execute("DELETE FROM asignaturas WHERE id = %s", (id,))
                conexion.commit()

                # Eliminar carpetas relacionadas
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
            # Obtener curso_id y nombre de la asignatura
            cursor.execute("SELECT curso_id, asignatura FROM asignaturas WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                curso_id, nombre_asignatura = result

                # 1. Eliminar todas las pruebas asociadas a la asignatura
                cursor.execute("DELETE FROM pruebas WHERE asignatura_id = %s", (id,))

                # 2. Eliminar la asignatura
                cursor.execute("DELETE FROM asignaturas WHERE id = %s", (id,))
                conexion.commit()

                # 3. Eliminar carpetas relacionadas (formato y alumnos)
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
