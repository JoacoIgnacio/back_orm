import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    try:
        return pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT'))
        )
    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None