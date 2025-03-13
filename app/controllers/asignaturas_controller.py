from app.BD.conexion import obtener_conexion
import json
from typing import List, Dict

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
    asignaturas = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM asignaturas WHERE curso_id = %s"
            cursor.execute(sql, (curso_id,))
            asignaturas = cursor.fetchall()
    except Exception as err:
        print(f'Error al obtener asignaturas para el curso con ID {curso_id}: {err}')
    finally:
        if conexion:
            conexion.close()
    
    return asignaturas

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
            asignatura = cursor.fetchone()  # Esto ya será un diccionario
            asignatura = {
                "id": asignatura[0],
                "asignatura": asignatura[1],
                "alternativas": asignatura[2],
                "preguntas": asignatura[3],
                "respuestas": asignatura[4],
                "curso_id": asignatura[5],
                "ruta_formato": asignatura[6]
            }
    except Exception as err:
        print(f'Error al obtener hoja de respuestas con ID {asignaturas_id}:', err)
    finally:
        if conexion:
            conexion.close()
    return asignatura

def obtener_asignaturas_por_id(id):
    asignatura = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM asignaturas WHERE id = %s"
            cursor.execute(sql, (id,))
            asignatura = cursor.fetchone()  # Esto ya será un diccionario
            asignatura = {
                "id": asignatura[0],
                "asignatura": asignatura[1],
                "alternativas": asignatura[2],
                "preguntas": asignatura[3],
                "respuestas": asignatura[4],
                "curso_id": asignatura[5],
                "ruta_formato": asignatura[6],
                "total_columnas": asignatura[7]
            }
    except Exception as err:
        print(f'Error al obtener hoja de respuestas con ID {asignatura}:', err)
    finally:
        if conexion:
            conexion.close()
    return asignatura

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

def eliminar_asignaturas(asignaturas_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "DELETE FROM asignaturas WHERE id = %s"
            cursor.execute(sql, (asignaturas_id,))
        conexion.commit()
    except Exception as err:
        print(f'Error al eliminar hoja de respuestas con ID {asignaturas_id}:', err)
    finally:
        if conexion:
            conexion.close()
