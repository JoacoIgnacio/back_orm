# app/controllers/cursos_controllers.py
from app.BD.conexion import obtener_conexion

def crear_curso(curso):
    curso_id = None
    try:
        with obtener_conexion().cursor() as cursor:
            cursor.execute(
                "INSERT INTO cursos (curso, activo, user_id) VALUES (%s, %s, %s)",
                (curso['curso'], curso['activo'], curso['user_id'])
            )
            cursor.connection.commit()
            curso_id = cursor.lastrowid
    except Exception as err:
        print(f'Error al crear curso: {err}')
    return curso_id

def obtener_cursos_por_usuario(user_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            print(f"🔍 Obteniendo cursos para el usuario con ID: {user_id}")
            cursor.execute("SELECT id, curso, activo, user_id FROM cursos WHERE user_id = %s", (user_id,))
            resultados = cursor.fetchall()
            print(f"✅ Resultados obtenidos: {resultados}")

            # Verificar si se obtuvieron resultados
            if not resultados:
                print("❌ No se encontraron cursos para este usuario.")
                return []  # Retornar lista vacía

            # Retornar directamente los resultados si ya son diccionarios
            print(f"✅ Cursos devueltos: {resultados}")
            return resultados  # Retornar directamente los resultados sin modificar

    except Exception as err:
        print(f'🚨 Error al obtener cursos para el usuario con ID {user_id}: {err}')
        return []
    finally:
        if conexion:
            conexion.close()

def obtener_curso_por_id(curso_id):
    try:
        with obtener_conexion().cursor() as cursor:
            cursor.execute("SELECT * FROM cursos WHERE id = %s", (curso_id,))
            return cursor.fetchone()
    except Exception as err:
        print(f'Error al obtener curso con ID {curso_id}: {err}')
        return None

def obtener_curso_por_nombre(nombre):
    try:
        with obtener_conexion().cursor() as cursor:
            cursor.execute("SELECT * FROM cursos WHERE curso = %s", (nombre,))
            return cursor.fetchone()
    except Exception as err:
        print(f'Error al obtener curso con nombre {nombre}: {err}')
        return None

def actualizar_curso(curso_id, nuevos_datos):
    try:
        with obtener_conexion().cursor() as cursor:
            cursor.execute(
                "UPDATE cursos SET curso = %s, activo = %s WHERE id = %s",
                (nuevos_datos['curso'], nuevos_datos['activo'], curso_id)
            )
            cursor.connection.commit()
    except Exception as err:
        print(f'Error al actualizar curso con ID {curso_id}: {err}')

def eliminar_curso(curso_id):
    try:
        with obtener_conexion().cursor() as cursor:
            cursor.execute("DELETE FROM cursos WHERE id = %s", (curso_id,))
            cursor.connection.commit()
    except Exception as err:
        print(f'Error al eliminar curso con ID {curso_id}: {err}')
