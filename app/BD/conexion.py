import pymysql

def obtener_conexion():
    return pymysql.connect(
        host='viaduct.proxy.rlwy.net',
        user='root',
        password='mcmMRVpFneUmNZSbZUNwZbtMQwTRaPUV',  # Agrega tu contraseña real aquí
        db='railway',
        port=29038  # Asegúrate de que el puerto sea el correcto
    )
