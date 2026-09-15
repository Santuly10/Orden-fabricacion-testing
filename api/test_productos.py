import requests


def test_listar_productos_responde_200(api_url):
    response = requests.get(f"{api_url}/api/productos", timeout=5)

    assert response.status_code == 200, (
        f"Se esperaba HTTP 200, pero llegó {response.status_code}. "
        f"Respuesta: {response.text}"
    )


def test_listar_productos_devuelve_lista(api_url):
    response = requests.get(f"{api_url}/api/productos", timeout=5)

    assert response.status_code == 200

    datos = response.json()

    assert isinstance(datos, list), (
        f"Se esperaba una lista JSON, pero llegó: {type(datos).__name__}. "
        f"Contenido: {datos}"
    )
