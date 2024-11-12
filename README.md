# Powerplant Load Management API

Este servicio acepta una solicitud POST con un payload JSON que contiene información sobre la carga de energía, los combustibles y las plantas de energía. Está diseñado para procesar los datos y devolver una respuesta.

https://github.com/gems-st-ib/powerplant-coding-challenge/tree/master

## Requisitos Previos

Asegúrate de tener los siguientes programas instalados en tu sistema:
- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation) (para la gestión de dependencias)
- Docker (para contenerización) -- Opcional

## Configuración del Proyecto

### 1. Descargar proyecto desde Wetranfer

Descargar y descomrpime el zip del proyecto a tu máquina local y navega al directorio del proyecto:

```bash
cd powerplant-api
```

### 2. Instalar las Dependencias

Para instalar las dependencias del proyecto, usa [Poetry](https://python-poetry.org/):

```bash
poetry install
```

### 3. Ejecutar la API Localmente

Para ejecutar el servicio localmente usando Poetry:

```bash
poetry run python -m powerplant_api.app
```

La API estará disponible en `http://localhost:8888`.

## Ejecutar la API con Docker

### 1. Construir la Imagen de Docker

Para construir la imagen Docker de la API, ejecuta el siguiente comando en el directorio del proyecto:

```bash
docker build -t powerplant-api .
```

### 2. Ejecutar el Contenedor Docker

Después de construir la imagen, puedes ejecutar el contenedor con el siguiente comando:

```bash
docker run -p 8888:8888 powerplant-api
```

Esto iniciará la API en `http://localhost:8888`.

## Ejecución de Pruebas

Para ejecutar las pruebas, utiliza el siguiente comando:

```bash
python -m unittest discover -s tests
```

### 3. Estructura de Pruebas

Las pruebas se encuentran en la carpeta `tests`, y están diseñadas para verificar el funcionamiento de la API y su lógica de negocio.

### Información sobre las Pruebas

- Cada prueba está escrita utilizando el marco de pruebas `unittest`.
- Las pruebas se configuran en el método `setUp`, que inicializa un cliente de prueba para la API.
- Se pueden agregar más pruebas en el archivo `test_app.py` según sea necesario.

## Endpoint de la API

### POST `/productionplan`

El endpoint `/productionplan` acepta una solicitud POST con un payload JSON en el siguiente formato:

```json
{
  "load": 480,
  "fuels": {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    {
      "name": "gasfiredbig1",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    ...
  ]
}
```

#### Respuesta de Ejemplo

La respuesta reflejará el payload recibido, con un status de éxito:

```json
{
  "status": "success",
  "received_load": 480,
  "fuels": {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [...]
}
```

## Notas

- Asegúrate de que el puerto 8888 esté disponible en tu máquina local para evitar conflictos.