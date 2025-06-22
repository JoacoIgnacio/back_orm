<<<<<<< HEAD
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Leer configuración desde variables de entorno (definidas en cPanel)
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "railway")

# Configurar la conexión a la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
    return "✅ Flask conectado correctamente a MySQL ✅ "

@app.route("/db-test")
def db_test():
    try:
        db.session.execute("SELECT 1")
        return "✅ Conexión a la base de datos exitosa"
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    app.run()
=======
from app import app
# Agregar esto al final para que Flask pueda detectar 'app'
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

>>>>>>> parent of 7ad2f19 (Update app.py)
