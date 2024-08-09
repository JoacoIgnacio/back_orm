# app/DB/controllers/pruebas_controller.py
from app.BD.conexion import obtener_conexion

def crear_prueba(prueba):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "INSERT INTO pruebas (nota, respuestas, activo, asignatura_id, alumno_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (prueba['nota'], prueba['respuestas'], prueba['activo'], prueba['asignatura_id'], prueba['alumno_id']))
            conexion.commit()
    except Exception as err:
        print('Error al crear prueba:', err)
    finally:
        if conexion:
            conexion.close()
            
def obtener_pruebas():
    pruebas = []
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Obtener todas las pruebas
            sql = "SELECT * FROM pruebas"
            cursor.execute(sql)
            pruebas = cursor.fetchall()
    except Exception as err:
        print('Error al obtener pruebas:', err)
    finally:
        if conexion:
            conexion.close()
    return pruebas

def obtener_prueba_por_id(prueba_id):
    resultados = []
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:

            cursor.execute("SELECT * FROM pruebas WHERE asignatura_id = %s", (prueba_id,))
            pruebas = cursor.fetchall()
            
            for prueba in pruebas:
                cursor.execute("SELECT * FROM alumnos WHERE id = %s", (prueba[5],))
                alumnos = cursor.fetchall()
                
                for alumno in alumnos:
                    resultado = {
                        "nombre": f"{alumno[1]} {alumno[2]}",
                        "nota": prueba[1],
                        "respuesta": prueba[2]
                    }
                    resultados.append(resultado)
            
        
    except Exception as err:
        print(f'Error al obtener prueba con ID {prueba_id}:', err)
    finally:
        if conexion:
            conexion.close()
    return resultados

def actualizar_prueba(prueba_id, nuevos_datos):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Actualizar una prueba por ID
            sql = "UPDATE pruebas SET nota = %s, activo = %s, id_hoja_de_respuestas = %s WHERE id = %s"
            cursor.execute(sql, (
                nuevos_datos['nota'],
                nuevos_datos['activo'],
                nuevos_datos['id_hoja_de_respuestas'],
                prueba_id
            ))
        conexion.commit()
    except Exception as err:
        print(f'Error al actualizar prueba con ID {prueba_id}:', err)
    finally:
        if conexion:
            conexion.close()

def eliminar_prueba(prueba_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Eliminar una prueba por ID
            sql = "DELETE FROM pruebas WHERE id = %s"
            cursor.execute(sql, (prueba_id,))
        conexion.commit()
    except Exception as err:
        print(f'Error al eliminar prueba con ID {prueba_id}:', err)
    finally:
        if conexion:
            conexion.close()
