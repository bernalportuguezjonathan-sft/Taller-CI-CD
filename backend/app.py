from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api')
def status():
    return jsonify({"status": "ok", "mensaje": "API de prueba funcionando perfectamente en Docker!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    