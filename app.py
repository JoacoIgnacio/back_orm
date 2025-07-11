import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# 👇 IMPORTA LA APP YA CONFIGURADA CON BLUEPRINTS
from app import app as application

load_dotenv()

# Leer configuración desde variables de entorno
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME")

# Configuración de la BD
application.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)

@application.route("/db-test")
def db_test():
    try:
        db.session.execute(text("SELECT 1"))
        return "✅ Conexión a la base de datos exitosa"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# No pongas application.run() en cPanel
