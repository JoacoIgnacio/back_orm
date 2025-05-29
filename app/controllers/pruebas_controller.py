# app/DB/controllers/pruebas_controller.py
from app.BD.conexion import obtener_conexion
import ast

def crear_prueba(prueba):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO pruebas (
                    respuestas, correctas, incorrectas, total_preguntas, activo, asignatura_id, alumno_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                prueba['respuestas'],
                prueba['correctas'],
                prueba['incorrectas'],
                prueba['total_preguntas'],
                prueba['activo'],
                prueba['asignatura_id'],
                prueba['alumno_id']
            ))

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
            sql = """
                UPDATE pruebas SET 
                    respuestas = %s,
                    correctas = %s,
                    incorrectas = %s,
                    total_preguntas = %s,
                    activo = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                nuevos_datos['respuestas'],
                nuevos_datos['correctas'],
                nuevos_datos['incorrectas'],
                nuevos_datos['total_preguntas'],
                nuevos_datos['activo'],
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

def obtener_notas_por_asignatura_controller(asignatura_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT pr.id, al.nombre, al.apellido, pr.correctas, pr.total_preguntas, pr.respuestas
                FROM pruebas pr
                JOIN alumnos al ON pr.alumno_id = al.id
                WHERE pr.asignatura_id = %s
            """, (asignatura_id,))
            resultados = cursor.fetchall()

            #print("Resultados consulta notas:", resultados)  # DEBUG

            notas = []
            for fila in resultados:
                try:
                    respuestas_raw = fila["respuestas"]

                    if isinstance(respuestas_raw, str):
                        respuestas_raw = respuestas_raw.strip().replace('[', '').replace(']', '')
                        respuestas = [int(r.strip()) for r in respuestas_raw.split(',') if r.strip().isdigit()]
                    elif isinstance(respuestas_raw, list):
                        respuestas = respuestas_raw
                    else:
                        respuestas = []

                    notas.append({
                        "id": fila["id"],
                        "nombre": fila["nombre"],
                        "apellido": fila["apellido"],
                        "correctas": fila["correctas"],
                        "total_preguntas": fila["total_preguntas"],
                        "respuestas": respuestas
                    })
                except Exception as err:
                    print(f"❌ Error al procesar fila: {fila} -> {err}")

            return notas
    except Exception as error:
        print(f"❌ Error al obtener notas: {error}")
        return []
