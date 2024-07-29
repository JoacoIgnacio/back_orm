from app.BD.conexion import obtener_conexion

def crear_usuario(usuario):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "INSERT INTO users (username, email, contrasena, activo) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (usuario['username'], usuario['email'], usuario['contrasena'], usuario['activo']))
        conexion.commit()
    except Exception as err:
        print('Error al crear usuario:', err)
    finally:
        if conexion:
            conexion.close()

def obtener_usuarios():
    usuarios = []
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            usuarios = cursor.fetchall()
    except Exception as err:
        print('Error al obtener usuarios:', err)
    finally:
        if conexion:
            conexion.close()
    return usuarios

def obtener_usuario_por_id(user_id):
    usuario = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            usuario = cursor.fetchone()
    except Exception as err:
        print(f'Error al obtener usuario con ID {user_id}:', err)
    finally:
        if conexion:
            conexion.close()
    return usuario

def actualizar_usuario(user_id, nuevos_datos):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "UPDATE users SET username = %s, email = %s, contrasena = %s, activo = %s WHERE id = %s"
            cursor.execute(sql, (nuevos_datos['username'], nuevos_datos['email'], nuevos_datos['contrasena'], nuevos_datos['activo'], user_id))
        conexion.commit()
    except Exception as err:
        print(f'Error al actualizar usuario con ID {user_id}:', err)
    finally:
        if conexion:
            conexion.close()

def eliminar_usuario(user_id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "DELETE FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
        conexion.commit()
    except Exception as err:
        print(f'Error al eliminar usuario con ID {user_id}:', err)
    finally:
        if conexion:
            conexion.close()
