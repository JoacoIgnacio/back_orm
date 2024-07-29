# app/DB/controllers/respuestas_alumnos_controller.py
import json
from app.BD.conexion import obtener_conexion

def agregar_respuestas_alumnos(respuestas):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Convertir los datos a una cadena JSON
            respuestas_json = json.dumps(respuestas)

            # Insertar en la tabla respuestas_alumnos
            sql = "INSERT INTO respuestas_alumnos (respuestas) VALUES (%s)"
            cursor.execute(sql, (respuestas_json,))
        conexion.commit()
    except Exception as err:
        print('Error al agregar respuestas de alumnos:', err)
    finally:
        if conexion:
            conexion.close()

def obtener_respuestas_alumnos():
    respuestas_alumnos = []
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Obtener todas las respuestas de alumnos
            sql = "SELECT * FROM respuestas_alumnos"
            cursor.execute(sql)
            respuestas_alumnos = cursor.fetchall()
    except Exception as err:
        print('Error al obtener respuestas de alumnos:', err)
    finally:
        if conexion:
            conexion.close()
    return respuestas_alumnos

# Puedes agregar funciones para actualizar y eliminar según sea necesario
