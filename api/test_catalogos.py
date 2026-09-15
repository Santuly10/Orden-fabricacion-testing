import requests
import pytest


@pytest.mark.parametrize(
    "recurso",
    [
        "materiales",
        "colores",
        "proveedores",
    ]
)
def test_listados_responden_200(api_url, recurso):
    response = requests.get(
        f"{api_url}/api/{recurso}",
        timeout=5
    )

    assert response.status_code == 200, (
        f"GET /api/{recurso} debería responder 200, "
        f"pero respondió {response.status_code}. "
        f"Respuesta: {response.text}"
    )


@pytest.mark.parametrize(
    "recurso",
    [
        "materiales",
        "colores",
        "proveedores",
    ]
)
def test_listados_devuelven_lista(api_url, recurso):
    response = requests.get(
        f"{api_url}/api/{recurso}",
        timeout=5
    )

    assert response.status_code == 200

    datos = response.json()

    assert isinstance(datos, list), (
        f"/api/{recurso} debería devolver una lista JSON, "
        f"pero devolvió {type(datos).__name__}: {datos}"
    )