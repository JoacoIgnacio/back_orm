# app/DB/controllers/cursos_controller.py
from app.BD.conexion import obtener_conexion
import shutil
import os

def crear_curso(curso):
    curso_id = None  # Inicializa aquí la variable
    conexion = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO cursos (curso, activo, user_id) VALUES (%s, %s, %s)",
            (curso['curso'], curso['activo'], curso['user_id'])
        )
        conexion.commit()
        curso_id = cursor.lastrowid
    except Exception as err:
        print('Error al crear curso:', err)
        curso_id = None
    finally:
        if conexion:
            conexion.close()
    return curso_id


def obtener_cursos_por_usuario(user_id):
    cursos = []
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Obtener todos los cursos asociados al usuario
            sql = "SELECT * FROM cursos WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            cursos = cursor.fetchall()
    except Exception as err:
        print(f'Error al obtener cursos para el usuario con ID {user_id}:', err)
    finally:
        if conexion:
            conexion.close()
    return cursos

def obtener_cursos():
    cursos = []
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Obtener todos los cursos
            sql = "SELECT * FROM cursos"
            cursor.execute(sql)
            cursos = cursor.fetchall()
    except Exception as err:
        print('Error al obtener cursos:', err)
    finally:
        if conexion:
            conexion.close()
    return cursos

def obtener_curso_por_id(curso_id):
    curso = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Obtener un curso por ID
            sql = "SELECT * FROM cursos WHERE id = %s"
            cursor.execute(sql, (curso_id,))
            curso = cursor.fetchone()  # Esto ya será un diccionario
            curso = {
                "id": curso[0],
                "curso": curso[1],
                "activo": curso[2],
                "user_id": curso[3]
            }
    except Exception as err:
        print(f'Error al obtener curso con ID {curso_id}:', err)
    finally:
        if conexion:
            conexion.close()
    return curso

def obtener_curso_por_nombre(nombre):
    curso = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Obtener un curso por ID
            sql = "SELECT * FROM cursos WHERE curso = %s"
            cursor.execute(sql, (nombre,))
            curso = cursor.fetchone()  # Esto ya será un diccionario
            curso = {
                "id": curso[0],
                "curso": curso[1],
                "activo": curso[2],
                "user_id": curso[3]
            }
    except Exception as err:
        print(f'Error al obtener curso con ID {curso}:', err)
    finally:
        if conexion:
            conexion.close()
    return curso

def actualizar_curso(curso_id, nuevos_datos):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Actualizar un curso por ID
            sql = "UPDATE cursos SET curso = %s, activo = %s, prueba_id = %s, user_id = %s WHERE id = %s"
            cursor.execute(sql, (
                nuevos_datos['curso'],
                nuevos_datos['activo'],
                nuevos_datos['user_id'],
                curso_id
            ))
        conexion.commit()
    except Exception as err:
        print(f'Error al actualizar curso con ID {curso_id}:', err)
    finally:
        if conexion:
            conexion.close()

def eliminar_curso(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM cursos WHERE id = %s", (id,))
            conexion.commit()

            # Borrar carpetas estáticas
            for carpeta in ["formato", "alumnos"]:
                ruta = os.path.join("static", carpeta, str(id))
                if os.path.exists(ruta):
                    shutil.rmtree(ruta)
    finally:
        conexion.close()
