# app/controllers/cursos_controllers.py
from app.BD.conexion import obtener_conexion
from app.controllers.alumnos_controller import eliminar_alumnos_por_curso
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
            cursor.execute("SELECT id, curso, activo, user_id FROM cursos WHERE user_id = %s", (user_id,))
            cursos = cursor.fetchall()
            return cursos if cursos else []
    except Exception as err:
        print(f'Error al obtener cursos para el usuario con ID {user_id}: {err}')
        return []
def obtener_curso_por_id(curso_id):
    try:
        with obtener_conexion().cursor() as cursor:
            cursor.execute("SELECT * FROM cursos WHERE id = %s", (curso_id,))
            return cursor.fetchone()
    except Exception as err:
        print(f'Error al obtener curso con ID {curso_id}: {err}')
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
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            print(f"🔍 Verificando existencia del curso con ID: {curso_id}")
            cursor.execute("SELECT id FROM cursos WHERE id = %s", (curso_id,))
            curso = cursor.fetchone()
            print(f"📌 Resultado de SELECT curso: {curso}")

            if not curso:
                print("⚠️ Curso no encontrado en la BD")
                return False, 0

            # Obtener asignaturas
            cursor.execute("SELECT id FROM asignaturas WHERE curso_id = %s", (curso_id,))
            asignaturas = cursor.fetchall()
            print(f"📋 Asignaturas encontradas: {asignaturas}")

            for asignatura in asignaturas:
                asignatura_id = asignatura[0] if isinstance(asignatura, tuple) else asignatura.get("id")
                print(f"🧹 Eliminando pruebas de asignatura {asignatura_id}")
                cursor.execute("DELETE FROM pruebas WHERE asignatura_id = %s", (asignatura_id,))

            print("🧹 Eliminando asignaturas del curso")
            cursor.execute("DELETE FROM asignaturas WHERE curso_id = %s", (curso_id,))

            print("🧹 Eliminando alumnos del curso")
            cursor.execute("DELETE FROM alumnos WHERE curso_id = %s", (curso_id,))
            alumnos_eliminados = cursor.rowcount

            print("🧹 Eliminando curso")
            cursor.execute("DELETE FROM cursos WHERE id = %s", (curso_id,))

            conexion.commit()
            return True, alumnos_eliminados
    except Exception as err:
        print(f'🚨 Error al eliminar curso con ID {curso_id}: {err}')
        return False, 0
    finally:
        if conexion:
            conexion.close()


