import os

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def db_config():
    return {
        "host": os.getenv("DB_HOST", "db"),
        "port": os.getenv("DB_PORT", "5432"),
        "dbname": os.getenv("POSTGRES_DB", "postgres"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", ""),
    }


@app.route('/')
def home():
    return "Error interno", 500


@app.route('/api')
def status():
    cfg = db_config()
    try:
        conn = psycopg2.connect(connect_timeout=5, **cfg)
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
        conn.close()
        return jsonify({
            "status": "ok",
            "mensaje": "Conexion exitosa a la base de datos",
            "motor": version.split(" on ")[0],
            "base_de_datos": cfg["dbname"],
            "host": cfg["host"],
        })
    except Exception as error:
        return jsonify({
            "status": "error",
            "mensaje": "No se pudo conectar a la base de datos",
            "detalle": str(error),
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # nosec B104 - necesario para exponer el puerto dentro del contenedor Docker
