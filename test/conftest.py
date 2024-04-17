import pytest
from flask import Flask
from app import app as flask_app  # Asegúrate de que flask_app es la instancia de Flask creada en tu app.py
from flaskext.mysql import MySQL
from dotenv import load_dotenv
import os

# Cargar las variables de entorno de prueba
load_dotenv('.env.test')

@pytest.fixture(scope='module')
def app():
    """Configure a new app instance for testing."""
    # Configurar la aplicación para las pruebas
    flask_app.config['TESTING'] = True
    flask_app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')
    flask_app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
    flask_app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DB_PASSWORD')
    flask_app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')
    flask_app.config['SERVER_NAME'] = 'localhost:5000'

    mysql = MySQL(flask_app)  # Asegúrate de que la configuración de MySQL se aplique correctamente

    with flask_app.app_context():
        yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def authenticated_client(client, test_user):
    with client:
        client.post('/se_connecter', data={
            'inputEmail': test_user.email,
            'inputPass': test_user.password
        })
        yield client

# Aquí podrías definir tus funciones de test usando el cliente de pruebas.
