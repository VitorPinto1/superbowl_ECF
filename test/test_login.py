from flask import session
from unittest.mock import patch

def test_login_success_user(client):
<<<<<<< HEAD
    response = client.post('/connexion/se_connecter', data={
=======
    response = client.post('/se_connecter', data={
>>>>>>> a3e0e0fa2c39cf2a670b65321624fee6cd70f88d
        'inputEmail': 'testuser@hotmail.com',
        'inputPass': 'Testuser1#'
    }, follow_redirects=False)  
    assert response.status_code == 302
    assert '/espace_utilisateur' in response.location  

def test_login_success_admin(client):
<<<<<<< HEAD
    response = client.post('/connexion/se_connecter', data={
=======
    response = client.post('/se_connecter', data={
>>>>>>> a3e0e0fa2c39cf2a670b65321624fee6cd70f88d
        'inputEmail': 'adminuser@hotmail.com',
        'inputPass': 'Adminuser1#'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert '/espace_administrateur' in response.location  


def test_login_user_not_exist(client):

<<<<<<< HEAD
    response = client.post('/connexion/se_connecter', data={
=======
    response = client.post('/se_connecter', data={
>>>>>>> a3e0e0fa2c39cf2a670b65321624fee6cd70f88d
        'inputEmail': 'noexist@example.com',
        'inputPass': 'fakepassword'
    }, follow_redirects=True)

    assert response.status_code == 200

    html_content = response.data.decode()
    expected_error_msg = "L&#39;adresse e-mail ou le mot de passe est incorrect."
    assert expected_error_msg in html_content, f"Expected error message not found! Received content: {html_content}"

def test_login_unconfirmed_user(client):
<<<<<<< HEAD
    response = client.post('/connexion/se_connecter', data={
=======
    response = client.post('/se_connecter', data={
>>>>>>> a3e0e0fa2c39cf2a670b65321624fee6cd70f88d
        'inputEmail': 'notconfirmed@hotmail.com',
        'inputPass': 'Pocholo1#'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Veuillez confirmer votre compte avant de vous connecter." in response.get_data(as_text=True)

  
def test_session_creation_on_login(client):
    with client:
<<<<<<< HEAD
        client.post('/connexion/se_connecter', data={
=======
        client.post('/se_connecter', data={
>>>>>>> a3e0e0fa2c39cf2a670b65321624fee6cd70f88d
            'inputEmail': 'testuser@hotmail.com',
            'inputPass': 'Testuser1#'
        }, follow_redirects=True)
        assert 'id_utilisateur' in session


def test_login_with_empty_data(client):
<<<<<<< HEAD
    response = client.post('/connexion/se_connecter', data={
=======
    response = client.post('/se_connecter', data={
>>>>>>> a3e0e0fa2c39cf2a670b65321624fee6cd70f88d
        'inputEmail': '',
        'inputPass': ''
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "L&#39;adresse e-mail ou le mot de passe est incorrect." in response.get_data(as_text=True)
