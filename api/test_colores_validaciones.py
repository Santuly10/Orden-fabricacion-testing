import pytest
import requests


@pytest.mark.xfail(
    reason="La API actualmente permite crear colores vacíos",
    strict=True
)

def test_no_permite_color_vacio(api_url):
    response = requests.post(
        f"{api_url}/api/colores",
        json={
            "color": ""
        },
        timeout=5
    )

    # Si la API cometió el error de crear el color vacío,
    # lo eliminamos para no dejar basura en la base.
    if response.status_code in (200, 201):
        try:
            datos = response.json()
            id_color = datos.get("id_color")

            if id_color:
                requests.delete(
                    f"{api_url}/api/colores/{id_color}",
                    timeout=5
                )
        except ValueError:
            pass

    assert response.status_code in (400, 422), (
        "La API debería rechazar un color vacío.\n"
        f"Status recibido: {response.status_code}\n"
        f"Respuesta: {response.text}"
    )