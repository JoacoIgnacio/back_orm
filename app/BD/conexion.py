#import pymysql
#import os
#from dotenv import load_dotenv

#load_dotenv()

# Verificar si usamos Railway o MySQL local
#USE_RAILWAY = os.getenv('USE_RAILWAY') == 'True'

#def obtener_conexion():
#    try:
#        return pymysql.connect(
#            host=os.getenv('DB_HOST') if USE_RAILWAY else "localhost",
#            user=os.getenv('DB_USER') if USE_RAILWAY else "root",
#            password=os.getenv('DB_PASSWORD') if USE_RAILWAY else "",
#            db=os.getenv('DB_NAME') if USE_RAILWAY else "lectoromr",
#            port=int(os.getenv('DB_PORT')) if USE_RAILWAY else 3306,
#            ssl={"ssl": {}} if USE_RAILWAY else None  # Railway necesita SSL
#        )
#    except pymysql.MySQLError as e:
#        print(f"❌ Error al conectar a la base de datos: {e}")
#        return None 

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
            connect_timeout=30  # Evita timeout por inactividad
        )
        return conexion
    except pymysql.MySQLError as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None


