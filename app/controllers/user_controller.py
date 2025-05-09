from app.BD.conexion import obtener_conexion
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def verificar_credenciales(email, contrasena):
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT id, username, email, contrasena, activo FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            usuario = cursor.fetchone()

            if usuario:
                print("Usuario encontrado en login:", usuario)  # ✅ Verificar el usuario obtenido
                print("Contraseña ingresada:", contrasena)
                print("Hash almacenado:", usuario['contrasena'])

                if bcrypt.check_password_hash(usuario['contrasena'], contrasena):
                    print("✅ Contraseña correcta")
                    return usuario
                else:
                    print("❌ Contraseña incorrecta")
                    return None
    finally:
        conexion.close()
    return None

def crear_usuario(usuario):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            contrasena_hash = bcrypt.generate_password_hash(usuario['contrasena']).decode('utf-8')
            sql = "INSERT INTO users (username, email, contrasena, activo) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (
                usuario['username'],
                usuario['email'],
                contrasena_hash,
                usuario.get('activo', True)
            ))
        conexion.commit()
    except Exception as err:
        print('Error al crear usuario:', err)
    finally:
        if conexion:
            conexion.close()

def obtener_usuario_por_id(user_id):
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor() as cursor:  # ✅ DictCursor ya está configurado en la conexión
            sql = "SELECT username, email FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            usuario = cursor.fetchone()
            print("Usuario encontrado:", usuario)  # Verificar el resultado
    finally:
        conexion.close()
    return usuario

def obtener_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT id, username, email FROM users"
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            print("Usuarios encontrados:", usuarios)
    finally:
        conexion.close()
    return usuarios



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
