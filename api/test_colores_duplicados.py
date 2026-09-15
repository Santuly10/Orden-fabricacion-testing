import pytest
import requests
import uuid


@pytest.mark.xfail(
    reason="La API devuelve 500 ante colores duplicados en lugar de 400/409",
    strict=True
)

def test_no_permite_color_duplicado(api_url):
    nombre = f"TEST_DUPLICADO_{uuid.uuid4().hex[:6]}"

    id_color_original = None
    id_color_duplicado = None

    try:
        # ==========================================
        # 1. Crear el primer color
        # ==========================================

        response_1 = requests.post(
            f"{api_url}/api/colores",
            json={
                "color": nombre
            },
            timeout=5
        )

        assert response_1.status_code in (200, 201), (
            f"No se pudo crear el color inicial.\n"
            f"Status: {response_1.status_code}\n"
            f"Respuesta: {response_1.text}"
        )

        datos_1 = response_1.json()
        id_color_original = datos_1.get("id_color")

        # ==========================================
        # 2. Intentar crear exactamente el mismo
        # ==========================================

        response_2 = requests.post(
            f"{api_url}/api/colores",
            json={
                "color": nombre
            },
            timeout=5
        )

        # Si por algún motivo también lo creó,
        # guardamos el ID para poder limpiarlo.
        if response_2.status_code in (200, 201):
            try:
                datos_2 = response_2.json()
                id_color_duplicado = datos_2.get("id_color")
            except ValueError:
                pass

        # ==========================================
        # 3. Validar
        # ==========================================

        assert response_2.status_code in (400, 409, 422), (
            "La API debería rechazar un color duplicado.\n"
            f"Status recibido: {response_2.status_code}\n"
            f"Respuesta: {response_2.text}"
        )

    finally:
        # ==========================================
        # LIMPIEZA
        # ==========================================

        if id_color_duplicado is not None:
            requests.delete(
                f"{api_url}/api/colores/{id_color_duplicado}",
                timeout=5
            )

        if id_color_original is not None:
            requests.delete(
                f"{api_url}/api/colores/{id_color_original}",
                timeout=5
            )