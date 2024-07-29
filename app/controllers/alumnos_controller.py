from app.BD.conexion import obtener_conexion
from app.routes.routes_qr import generar_qr_imagen
from flask import jsonify

def crear_alumno(alumno):
    qr_info = None
    try:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                # Insertar el nuevo alumno
                sql_insert = "INSERT INTO alumnos (nombre, apellido, QR, id_curso) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_insert, (
                    alumno['nombre'],
                    alumno['apellido'],
                    alumno['QR'],
                    alumno['id_curso']
                ))
                
                # Obtener el ID del alumno recién creado
                cursor.execute("SELECT LAST_INSERT_ID()")
                id_alumno = cursor.fetchone()[0]

                # Crear la información del QR
                qr_info = {
                    "nombre": alumno['nombre'],
                    "apellido": alumno['apellido'],
                    "id_curso": alumno['id_curso'],
                    "id_alumno": id_alumno
                }

                # Generar la imagen del QR
                qr_path2 = generar_qr_imagen(
                    alumno['nombre'],
                    alumno['apellido'],
                    qr_info
                )

                # Actualizar la fila del alumno con la nueva información del QR
                sql_update = "UPDATE alumnos SET QR = %s WHERE id = %s"
                cursor.execute(sql_update, (qr_path2['ruta_qr'], id_alumno))

            # Confirmar la transacción
            conexion.commit()

    except Exception as err:
        print(f'Error al crear alumno: {err}')
        try:
            if conexion and not conexion.closed:
                conexion.rollback()
        except Exception as rollback_err:
            print(f'Error al hacer rollback: {rollback_err}')
    
    return {"nombre": alumno['nombre'], "apellido": alumno['apellido'], "id_curso": alumno['id_curso'], "id_alumno": id_alumno, "qr": qr_path2['ruta_qr']}




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

def obtener_alumnos_por_curso(id_curso):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Consultar todos los alumnos de un curso específico
            sql = "SELECT * FROM alumnos WHERE id_curso = %s"
            cursor.execute(sql, (id_curso,))
            alumnos = cursor.fetchall()
        print(alumnos)
        return alumnos
    except Exception as err:
        print(f'Error al obtener alumnos por curso {id_curso}: {err}')
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
            cursor.execute("SELECT id_curso FROM alumnos WHERE id = %s", (alumno_id,))
            id_curso_actual = cursor.fetchone()[0]

            # Actualizar un alumno por ID
            sql = "UPDATE alumnos SET nombre = %s, apellido = %s, QR = %s, id_curso = %s WHERE id = %s"

            # Genera un nuevo QR
            nuevo_qr_info = f"nombre: {nuevos_datos['nombre']}\napellido: {nuevos_datos['apellido']}\nid_curso: {id_curso_actual}\nid_alumno: {alumno_id}"
            nuevo_qr = generar_qr_imagen(
                nuevos_datos['nombre'],
                nuevos_datos['apellido'],
                nuevo_qr_info
            )

            # Extrae la ruta del QR del diccionario
            nuevo_qr_ruta = nuevo_qr.get('ruta_qr', '')

            cursor.execute(sql, (
                nuevos_datos['nombre'],
                nuevos_datos['apellido'],
                nuevo_qr_ruta,  # Pasa solo la ruta del QR, no el diccionario completo
                id_curso_actual,  # Usa el ID del curso actual
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

def eliminar_alumnos_por_curso(id_curso):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Eliminar alumnos por id_curso
            sql = "DELETE FROM alumnos WHERE id_curso = %s"
            cursor.execute(sql, (id_curso,))
        conexion.commit()
    except Exception as err:
        print(f'Error al eliminar alumnos por curso con ID {id_curso}:', err)
    finally:
        if conexion:
            conexion.close()            