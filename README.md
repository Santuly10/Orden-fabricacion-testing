# Orden-fabricacion-testing

Suite de testing automatizado externa para el proyecto grupal **Orden de Fabricación**.

Este proyecto NO modifica el código del proyecto original. Consume la API Flask como un cliente externo.

## 1. Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3. Levantar el backend original

En otra terminal, dentro del proyecto `Orden-de-fabricacion/backend`, activar su entorno virtual y ejecutar Flask normalmente.

Ejemplo:

```bash
source venv/bin/activate
python app.py
```

La suite supone por defecto que la API está en:

```text
http://127.0.0.1:5000
```

Si usa otra URL:

```bash
API_URL=http://localhost:5001 pytest
```

## 4. Ejecutar los tests

```bash
pytest
```

o:

```bash
pytest -v
```

## Primeros tests incluidos

- `GET /api/productos` debe responder HTTP 200.
- `GET /api/productos` debe devolver una lista JSON.
