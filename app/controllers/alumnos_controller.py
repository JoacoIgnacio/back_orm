from app.BD.conexion import obtener_conexion
from flask import jsonify

def crear_alumno(alumno):
    try:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                # Verificar si el curso existe antes de crear el alumno
                cursor.execute("SELECT id FROM cursos WHERE id = %s", (alumno['curso_id'],))
                curso_existente = cursor.fetchone()
                if not curso_existente:
                    print(f"Error: El curso con ID {alumno['curso_id']} no existe.")
                    return {"error": "El curso especificado no existe."}

                # Insertar el nuevo alumno
                sql_insert = "INSERT INTO alumnos (nombre, apellido, curso_id) VALUES (%s, %s, %s)"
                cursor.execute(sql_insert, (
                    alumno['nombre'],
                    alumno['apellido'],
                    alumno['curso_id']
                ))
                
                alumno_id = cursor.lastrowid
            # Confirmar la transacción
            conexion.commit()
            
            alumno_creado = {
                'id': alumno_id,
                'nombre': alumno['nombre'],
                'apellido': alumno['apellido'],
                'curso_id': alumno['curso_id']
            }
            return alumno_creado

    except Exception as err:
        print(f'Error al crear alumno: {err}')
        return {"error": str(err)}

def obtener_alumnos():
    alumnos = []
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Obtener todos los alumnos
            sql = "SELECT * FROM alumnos"
            cursor.execute(sql)
            alumnos = cursor.fetchall()
    except Exception as err:
        print('Error al obtener alumnos:', err)
    finally:
        if conexion:
            conexion.close()
    return alumnos

def obtener_alumnos_por_curso(curso_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Consultar todos los alumnos de un curso específico
            sql = "SELECT * FROM alumnos WHERE curso_id = %s"
            cursor.execute(sql, (curso_id,))
            alumnos = cursor.fetchall()
        return alumnos
    except Exception as err:
        print(f'Error al obtener alumnos por curso {curso_id}: {err}')
        return []
    finally:
        if conexion:
            conexion.close()
            
def obtener_alumno_por_id(alumno_id):
    alumno = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Obtener un alumno por ID
            sql = "SELECT * FROM alumnos WHERE id = %s"
            cursor.execute(sql, (alumno_id,))
            alumno = cursor.fetchone()
    except Exception as err:
        print(f'Error al obtener alumno con ID {alumno_id}:', err)
    finally:
        if conexion:
            conexion.close()
    return alumno

def actualizar_alumno(alumno_id, nuevos_datos):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Verificar si el curso especificado existe
            cursor.execute("SELECT id FROM cursos WHERE id = %s", (nuevos_datos['curso_id'],))
            curso_existente = cursor.fetchone()
            if not curso_existente:
                print(f"Error: El curso con ID {nuevos_datos['curso_id']} no existe.")
                return {"error": "El curso especificado no existe."}

            # Actualizar un alumno por ID
            sql = "UPDATE alumnos SET nombre = %s, apellido = %s, curso_id = %s WHERE id = %s"
            cursor.execute(sql, (
                nuevos_datos['nombre'],
                nuevos_datos['apellido'],
                nuevos_datos['curso_id'],
                alumno_id
            ))

        conexion.commit()
        return True
    except Exception as err:
        print(f'Error al actualizar alumno con ID {alumno_id}:', err)
        return False

def eliminar_alumno(alumno_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Eliminar un alumno por ID
            sql = "DELETE FROM alumnos WHERE id = %s"
            cursor.execute(sql, (alumno_id,))
        conexion.commit()
    except Exception as err:
        print(f'Error al eliminar alumno con ID {alumno_id}:', err)
    finally:
        if conexion:
            conexion.close()

def eliminar_alumnos_por_curso(curso_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Eliminar alumnos por curso_id
            sql = "DELETE FROM alumnos WHERE curso_id = %s"
            cursor.execute(sql, (curso_id,))
        conexion.commit()
        print(f'Alumnos del curso {curso_id} eliminados correctamente.')
    except Exception as err:
        print(f'Error al eliminar alumnos por curso con ID {curso_id}: {err}')
    finally:
        if conexion:
            conexion.close()
