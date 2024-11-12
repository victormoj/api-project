# Usar una imagen base de Python 3.12
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de configuración de Poetry
COPY pyproject.toml poetry.lock* /app/

# Instalar Poetry
RUN pip install poetry

# Instalar las dependencias
RUN poetry install --no-root --no-dev

# Copiar el resto de la aplicación
COPY . /app

# Exponer el puerto
EXPOSE 8888

# Comando para ejecutar la aplicación
CMD ["poetry", "run", "python", "powerplant_api/app.py"]
