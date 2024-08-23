from app.BD.conexion import obtener_conexion
from flask import jsonify

def crear_alumno(alumno):
    try:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
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
        try:
            if conexion and not conexion.closed:
                conexion.rollback()
        except Exception as rollback_err:
            print(f'Error al hacer rollback: {rollback_err}')
        return False




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
            # Obtén el ID del curso actual para mantenerlo
            cursor.execute("SELECT curso_id FROM alumnos WHERE id = %s", (alumno_id,))
            curso_id_actual = cursor.fetchone()[0]

            # Actualizar un alumno por ID
            sql = "UPDATE alumnos SET nombre = %s, apellido = %s, curso_id = %s WHERE id = %s"

            cursor.execute(sql, (
                nuevos_datos['nombre'],
                nuevos_datos['apellido'],
                curso_id_actual,  # Usa el ID del curso actual
                alumno_id
            ))

        conexion.commit()
    except Exception as err:
        print(f'Error al actualizar alumno con ID {alumno_id}:', err)
    finally:
        if conexion:
            conexion.close()

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
    except Exception as err:
        print(f'Error al eliminar alumnos por curso con ID {curso_id}:', err)
    finally:
        if conexion:
            conexion.close()            