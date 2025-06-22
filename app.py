import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

load_dotenv()

application = Flask(__name__)

# Leer configuración desde variables de entorno (definidas en cPanel)
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME")

# Configurar la conexión a la base de datos
application.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)

@application.route("/")
def index():
    return "✅ Flask conectado correctamente a MySQL ✅ "

@application.route("z1")
def db_test():
    try:
        db.session.execute(text("SELECT 1"))
        return "✅ Conexión a la base de datos exitosa"
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    application.run()
