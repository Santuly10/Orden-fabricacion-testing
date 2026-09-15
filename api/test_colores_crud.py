import requests
import uuid


def test_crud_color_completo(api_url):
    # Generamos un nombre distinto cada vez que corre el test.
    # Ejemplo: TEST_COLOR_a81f6c
    nombre_original = f"TEST_COLOR_{uuid.uuid4().hex[:6]}"
    nombre_modificado = f"{nombre_original}_EDITADO"

    id_color = None

    try:
        # =====================================================
        # 1. CREATE - Crear un color
        # =====================================================

        response = requests.post(
            f"{api_url}/api/colores",
            json={
                "color": nombre_original
            },
            timeout=5
        )

        assert response.status_code in (200, 201), (
            f"No se pudo crear el color.\n"
            f"Status: {response.status_code}\n"
            f"Respuesta: {response.text}"
        )

        # =====================================================
        # 2. READ - Comprobar que fue creado
        # =====================================================

        response = requests.get(
            f"{api_url}/api/colores",
            timeout=5
        )

        assert response.status_code == 200

        colores = response.json()

        color_creado = next(
            (
                color
                for color in colores
                if color.get("color") == nombre_original
            ),
            None
        )

        assert color_creado is not None, (
            f"El color {nombre_original} fue creado "
            f"pero no aparece en GET /api/colores"
        )

        id_color = color_creado["id_color"]

        # =====================================================
        # 3. UPDATE - Modificar el color
        # =====================================================

        response = requests.put(
            f"{api_url}/api/colores/{id_color}",
            json={
                "color": nombre_modificado
            },
            timeout=5
        )

        assert response.status_code in (200, 204), (
            f"No se pudo modificar el color.\n"
            f"Status: {response.status_code}\n"
            f"Respuesta: {response.text}"
        )

        # Comprobamos que realmente cambió
        response = requests.get(
            f"{api_url}/api/colores",
            timeout=5
        )

        colores = response.json()

        color_editado = next(
            (
                color
                for color in colores
                if color.get("id_color") == id_color
            ),
            None
        )

        assert color_editado is not None

        assert color_editado["color"] == nombre_modificado, (
            f"Se esperaba {nombre_modificado}, "
            f"pero llegó {color_editado['color']}"
        )

        # =====================================================
        # 4. DELETE - Eliminar el color
        # =====================================================

        response = requests.delete(
            f"{api_url}/api/colores/{id_color}",
            timeout=5
        )

        assert response.status_code in (200, 204), (
            f"No se pudo eliminar el color.\n"
            f"Status: {response.status_code}\n"
            f"Respuesta: {response.text}"
        )

        # Como ya fue eliminado, evitamos intentar
        # borrarlo nuevamente en finally.
        id_color = None

        # =====================================================
        # 5. COMPROBAR QUE YA NO EXISTE
        # =====================================================

        response = requests.get(
            f"{api_url}/api/colores",
            timeout=5
        )

        colores = response.json()

        existe = any(
            color.get("color") == nombre_modificado
            for color in colores
        )

        assert existe is False, (
            "El color debería haber sido eliminado, "
            "pero todavía aparece en el listado."
        )

    finally:
        # =====================================================
        # LIMPIEZA
        # =====================================================
        # Si el test falla después de haber creado el color,
        # intentamos eliminarlo para no dejar datos TEST.
        if id_color is not None:
            requests.delete(
                f"{api_url}/api/colores/{id_color}",
                timeout=5
            )