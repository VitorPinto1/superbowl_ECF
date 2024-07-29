import pytest
from flask import Flask



from flaskext.mysql import MySQL

from dotenv import load_dotenv
import os

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.app import app as flask_app  

os.environ['FLASK_ENV'] = 'test'
# Charger les variables d'environnement de test
load_dotenv('.env.test')
print(os.environ['FLASK_ENV'])
@pytest.fixture(scope='module')
def app():
    
    # Configurer l'application pour les tests
    flask_app.config['TESTING'] = True
    flask_app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    flask_app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    flask_app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    flask_app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE')
    flask_app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
    flask_app.config['SERVER_NAME'] = 'localhost:5001'

    print("Configuraciones de la base de datos para pruebas:")
    print("MYSQL_HOST:", flask_app.config['MYSQL_HOST'])
    print("MYSQL_USER:", flask_app.config['MYSQL_USER'])
    print("MYSQL_PASSWORD:", flask_app.config['MYSQL_PASSWORD'])
    print("MYSQL_DB:", flask_app.config['MYSQL_DB'])
    print("MYSQL_PORT:", flask_app.config['MYSQL_PORT'])

    mysql = MySQL(flask_app)  

    try:
        with flask_app.app_context():
            yield flask_app
    except Exception as e:
        print(f"Error during app fixture setup: {e}")
    finally:
        try:
            if hasattr(mysql, 'connection') and mysql.connection.open:
                mysql.connection.close()
        except Exception as e:
            print(f"Error during MySQL connection close: {e}")


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def authenticated_client(client, test_user):
    with client:
        client.post('/se_connecter', data={
            'inputEmail': test_user.email,
            'inputPass': test_user.password
        })
        yield client

