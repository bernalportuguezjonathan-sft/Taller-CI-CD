from sample_app import sample


def test_ruta_principal_responde_200():
    cliente = sample.test_client()
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
