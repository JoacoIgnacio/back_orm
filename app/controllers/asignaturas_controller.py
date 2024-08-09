from app.BD.conexion import obtener_conexion
import json
from typing import List, Dict

def crear_asignaturas(asignaturas):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Convertir la lista de respuestas a una cadena JSON
            preguntas_json = json.dumps(asignaturas['preguntas'])
            respuestas_json = json.dumps(asignaturas['respuestas'])

            # Insertar nueva hoja de respuestas
            sql = "INSERT INTO asignaturas (asignatura, alternativas, preguntas, respuestas, curso_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (asignaturas['asignatura'], asignaturas['alternativas'], preguntas_json, respuestas_json, asignaturas['curso_id']))
        conexion.commit()
        print('Hoja de respuestas creada exitosamente')
    except Exception as err:
        print('Error al crear hoja de respuestas:', err)
    finally:
        if conexion:
            conexion.close()
    return {"asignatura": asignaturas['asignatura'], "alternativas": asignaturas['alternativas'], "preguntas": preguntas_json, "respuestas": respuestas_json, "curso_id": asignaturas['curso_id']}


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
    asignaturas = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM hoja_de_respuestas WHERE id = %s"
            cursor.execute(sql, (asignaturas_id,))
            asignaturas = cursor.fetchone()
    except Exception as err:
        print(f'Error al obtener hoja de respuestas con ID {asignaturas_id}:', err)
    finally:
        if conexion:
            conexion.close()
    return asignaturas

def actualizar_asignaturas(asignaturas_id, nuevos_datos):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "UPDATE hoja_de_respuestas SET asignatura = %s, alternativas = %s, preguntas = %s, respuestas = %s WHERE id = %s"
            cursor.execute(sql, (nuevos_datos['asignatura'], nuevos_datos['alternativas'], nuevos_datos['preguntas'], nuevos_datos['respuestas'], asignaturas_id))
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
