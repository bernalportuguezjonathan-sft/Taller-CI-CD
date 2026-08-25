from app import app


def test_ruta_principal_devuelve_200():
    cliente = app.test_client()
    respuesta = cliente.get("/")
    assert respuesta.status_code == 404  # fallo intencional para probar el bloqueo del pipeline
