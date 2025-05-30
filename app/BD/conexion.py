import pymysql
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def obtener_conexion():
    try:
        conexion = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT')),
            connect_timeout=30,  # Evita timeout por inactividad
            cursorclass=pymysql.cursors.DictCursor  # ✅ Asegura que sea DictCursor
        )
        return conexion
    except pymysql.MySQLError as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None
