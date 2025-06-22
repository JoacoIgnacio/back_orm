import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

# Leer configuración desde variables de entorno (definidas en cPanel)
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "railway")

# Configurar la conexión a la base de datos
application.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)

@application.route("/")
def index():
    return "✅ Flask conectado correctamente a MySQL ✅ "

@application.route("/db-test")
def db_test():
    try:
        db.session.execute("SELECT 1")
        return "✅ Conexión a la base de datos exitosa"
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    application.run()
