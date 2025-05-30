from app import app
# Agregar esto al final para que Flask pueda detectar 'app'
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

