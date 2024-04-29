# Usar una imagen base de Python
FROM python:3.9

# Define el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar las herramientas necesarias para compilar dependencias de Python que requieren compilación y 'dockerize'
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    wget \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requisitos y los archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que Flask utilizará
EXPOSE 5000

# Define environment variable
ENV NAME World

# Define el comando que se ejecutará al iniciar el contenedor, utilizando 'dockerize' para esperar a MySQL
ENTRYPOINT ["dockerize", "-wait", "tcp://db:3306", "-timeout", "20s"]
CMD ["python", "app.py"]
