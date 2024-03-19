# Usa la imagen oficial de Python
FROM python:3.8-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt ./
COPY script.py ./

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta el script al iniciar el contenedor
CMD ["python", "script.py"]
