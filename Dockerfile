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

ENV NAME World
ENV FLASK_APP ${FLASK_APP}
ENV FLASK_ENV ${FLASK_ENV}
ENV FLASK_DEBUG ${FLASK_DEBUG}
ENV DB_SECRETKEY ${DB_SECRETKEY}
ENV DB_PASSWORDEMAIL ${DB_PASSWORDEMAIL}
ENV DB_USER ${DB_USER}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV MAIL_PASSWORD ${MAIL_PASSWORD}
ENV MYSQL_ROOT_PASSWORD ${MYSQL_ROOT_PASSWORD}
ENV MYSQL_DATABASE_HOST ${MYSQL_DATABASE_HOST}

ENTRYPOINT ["dockerize", "-wait", "tcp://mysql-1afb9ef7-staniaprojets-ffa9.j.aivencloud.com:24978", "-timeout", "60s"]
CMD ["python", "/app/app.py"]

