"""
Aplicación web Flask - Actividad 4
Héctor García - UNIR
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """Ruta principal que devuelve un mensaje de saludo."""
    return jsonify({
        "mensaje": "¡Hola! Bienvenido a la aplicación Flask - Actividad 4",
        "autor": "Héctor García",
        "universidad": "UNIR",
        "status": "ok"
    })


@app.route("/health")
def health():
    """Endpoint de health check."""
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
