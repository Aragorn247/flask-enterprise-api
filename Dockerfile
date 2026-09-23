# 1. Imagen base ligera con Python 3.13
FROM python:3.13-slim

# 2. Previene que Python escriba archivos .pyc en disco y desactiva el buffering de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instala dependencias del sistema operativo requeridas por psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia el archivo de dependencias primero (para aprovechar la caché de Docker)
COPY requirements.txt /app/

# 6. Instala las librerías de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copia todo el código fuente del proyecto al contenedor
COPY . /app/

# 8. Expone el puerto en el que escuchará la aplicación Flask
EXPOSE 5000

# 9. Comando por defecto para iniciar el servidor de desarrollo de Flask
CMD ["python", "run.py"]