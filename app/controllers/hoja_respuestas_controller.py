from app.BD.conexion import obtener_conexion
import json
from typing import List, Dict

def crear_hoja_respuestas(hoja_respuestas):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Convertir la lista de respuestas a una cadena JSON
            preguntas_json = json.dumps(hoja_respuestas['preguntas'])
            respuestas_json = json.dumps(hoja_respuestas['respuestas'])

            # Insertar nueva hoja de respuestas
            sql = "INSERT INTO hojas_de_respuestas (asignatura, alternativas, preguntas, respuestas, usuario_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (hoja_respuestas['asignatura'], hoja_respuestas['alternativas'], preguntas_json, respuestas_json, hoja_respuestas['usuario_id']))
        conexion.commit()
        print('Hoja de respuestas creada exitosamente')
    except Exception as err:
        print('Error al crear hoja de respuestas:', err)
    finally:
        if conexion:
            conexion.close()
    return {"asignatura": hoja_respuestas['asignatura'], "alternativas": hoja_respuestas['alternativas'], "preguntas": preguntas_json, "respuestas": respuestas_json, "usuario_id": hoja_respuestas['usuario_id']}


def obtener_hojas_respuestas_por_usuario(usuario_id: int) -> List[Dict]:
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Obtener hojas de respuestas por usuario_id
            sql = "SELECT * FROM hojas_de_respuestas WHERE usuario_id = %s"
            cursor.execute(sql, (usuario_id,))
            hojas_respuestas = cursor.fetchall()

    except Exception as err:
        print(f'Error al obtener hojas de respuestas para el usuario con ID {usuario_id}: {err}')
    finally:
        if conexion:
            conexion.close()

    return hojas_respuestas

def obtener_hoja_respuestas():
    hojas_respuestas = []
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM hojas_de_respuestas"
            cursor.execute(sql)
            hojas_respuestas = cursor.fetchall()
    except Exception as err:
        print('Error al obtener hojas de respuestas:', err)
    finally:
        if conexion:
            conexion.close()
    return hojas_respuestas

def obtener_hoja_respuestas_por_id(hoja_respuestas_id):
    hoja_respuestas = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM hoja_de_respuestas WHERE id = %s"
            cursor.execute(sql, (hoja_respuestas_id,))
            hoja_respuestas = cursor.fetchone()
    except Exception as err:
        print(f'Error al obtener hoja de respuestas con ID {hoja_respuestas_id}:', err)
    finally:
        if conexion:
            conexion.close()
    return hoja_respuestas

def actualizar_hoja_respuestas(hoja_respuestas_id, nuevos_datos):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "UPDATE hoja_de_respuestas SET asignatura = %s, alternativas = %s, preguntas = %s, respuestas = %s WHERE id = %s"
            cursor.execute(sql, (nuevos_datos['asignatura'], nuevos_datos['alternativas'], nuevos_datos['preguntas'], nuevos_datos['respuestas'], hoja_respuestas_id))
        conexion.commit()
    except Exception as err:
        print(f'Error al actualizar hoja de respuestas con ID {hoja_respuestas_id}:', err)
    finally:
        if conexion:
            conexion.close()

def eliminar_hoja_respuestas(hoja_respuestas_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "DELETE FROM hojas_de_respuestas WHERE id = %s"
            cursor.execute(sql, (hoja_respuestas_id,))
        conexion.commit()
    except Exception as err:
        print(f'Error al eliminar hoja de respuestas con ID {hoja_respuestas_id}:', err)
    finally:
        if conexion:
            conexion.close()
