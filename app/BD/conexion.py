import pymysql

def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='claseac1_lectoromr',
        password='S%!=vj8sbpy9',  # Agrega tu contraseña real aquí
        db='claseac1_lectoromr'
    )
