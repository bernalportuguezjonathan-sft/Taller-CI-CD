import pymysql
import os
from flask import Flask, render_template, request, redirect, url_for

sample = Flask(__name__)

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'servidor-bd'),
    'user': os.getenv('DB_USER', 'root'),
    'passwd': os.getenv('DB_PASSWORD', '1234'),
    'database': os.getenv('DB_NAME', 'adso_db')
}

def get_db_connection():
    conn = pymysql.connect(**DB_CONFIG, autocommit=True)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aprendices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre_completo VARCHAR(100) NOT NULL,
            numero_documento VARCHAR(20) NOT NULL,
            ficha VARCHAR(20) NOT NULL,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.close()
    return conn

@sample.route('/', methods=['GET'])
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM aprendices ORDER BY creado_en DESC;")
        aprendices = cursor.fetchall()
        cursor.close()
        conn.close()
        db_status = "Conexión Exitosa"
    except Exception as e:
        aprendices = []
        db_status = f"Error de conexión: {e}"

    return render_template('index.html', aprendices=aprendices, db_status=db_status)

@sample.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre_completo')
    documento = request.form.get('numero_documento')
    ficha = request.form.get('ficha')

    if nombre and documento and ficha:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO aprendices (nombre_completo, numero_documento, ficha) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, documento, ficha))
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al registrar: {e}")

    return redirect(url_for('home'))

if __name__ == '__main__':
    sample.run(host='0.0.0.0', port=5050, debug=True)
