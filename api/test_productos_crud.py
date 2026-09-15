import requests
import uuid


def test_crud_producto_completo(api_url):
    codigo = uuid.uuid4().hex[:6]

    articulo_original = f"TEST-ART-{codigo}"
    nombre_original = f"Producto Test {codigo}"

    articulo_modificado = f"TEST-EDIT-{codigo}"
    nombre_modificado = f"Producto Editado {codigo}"

    id_producto = None

    # =====================================================
    # Primero obtenemos un color válido
    # =====================================================

    response_colores = requests.get(
        f"{api_url}/api/colores",
        timeout=5
    )

    assert response_colores.status_code == 200

    colores = response_colores.json()

    assert len(colores) > 0, (
        "Se necesita al menos un color existente "
        "para realizar el test de productos."
    )

    id_color = colores[0]["id_color"]

    try:

        # =====================================================
        # 1. CREATE
        # =====================================================

        response = requests.post(
            f"{api_url}/api/productos",
            json={
                "articulo_producto": articulo_original,
                "nombre_producto": nombre_original,
                "colores_id_color": id_color
            },
            timeout=5
        )

        assert response.status_code in (200, 201), (
            "No se pudo crear el producto.\n"
            f"Status: {response.status_code}\n"
            f"Respuesta: {response.text}"
        )

        # =====================================================
        # 2. READ
        # =====================================================

        response = requests.get(
            f"{api_url}/api/productos",
            timeout=5
        )

        assert response.status_code == 200

        productos = response.json()

        producto_creado = next(
            (
                producto
                for producto in productos
                if producto.get("articulo_producto")
                == articulo_original
            ),
            None
        )

        assert producto_creado is not None, (
            "El producto fue enviado por POST "
            "pero no aparece en el listado."
        )

        id_producto = producto_creado["id_producto"]

        assert producto_creado["nombre_producto"] == nombre_original
        assert producto_creado["colores_id_color"] == id_color

        # =====================================================
        # 3. UPDATE
        # =====================================================

        response = requests.put(
            f"{api_url}/api/productos/{id_producto}",
            json={
                "articulo_producto": articulo_modificado,
                "nombre_producto": nombre_modificado,
                "colores_id_color": id_color
            },
            timeout=5
        )

        assert response.status_code in (200, 204), (
            "No se pudo modificar el producto.\n"
            f"Status: {response.status_code}\n"
            f"Respuesta: {response.text}"
        )

        # =====================================================
        # Comprobar modificación
        # =====================================================

        response = requests.get(
            f"{api_url}/api/productos",
            timeout=5
        )

        productos = response.json()

        producto_editado = next(
            (
                producto
                for producto in productos
                if producto.get("id_producto") == id_producto
            ),
            None
        )

        assert producto_editado is not None

        assert producto_editado["articulo_producto"] == articulo_modificado
        assert producto_editado["nombre_producto"] == nombre_modificado

        # =====================================================
        # 4. DELETE
        # =====================================================

        response = requests.delete(
            f"{api_url}/api/productos/{id_producto}",
            timeout=5
        )

        assert response.status_code in (200, 204), (
            "No se pudo eliminar el producto.\n"
            f"Status: {response.status_code}\n"
            f"Respuesta: {response.text}"
        )

        id_producto = None

        # =====================================================
        # 5. COMPROBAR ELIMINACIÓN
        # =====================================================

        response = requests.get(
            f"{api_url}/api/productos",
            timeout=5
        )

        productos = response.json()

        existe = any(
            producto.get("articulo_producto")
            == articulo_modificado
            for producto in productos
        )

        assert existe is False, (
            "El producto fue eliminado "
            "pero todavía aparece en el listado."
        )

    finally:

        # =====================================================
        # LIMPIEZA
        # =====================================================

        if id_producto is not None:
            requests.delete(
                f"{api_url}/api/productos/{id_producto}",
                timeout=5
            )