from app import app


def test_ruta_principal_devuelve_200():
    cliente = app.test_client()
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200  # nosec B101 - pytest usa assert como su mecanismo normal de validacion
