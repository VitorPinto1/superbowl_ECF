FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    wget \
    default-mysql-client \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001





