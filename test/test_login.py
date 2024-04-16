

def test_login_success_user(client):
    response = client.post('/se_connecter', data={
        'inputEmail': 'testuser@hotmail.com',
        'inputPass': 'Testuser1#'
    }, follow_redirects=False)  
    assert response.status_code == 302
    assert '/espace_utilisateur' in response.location  # Verifica que la URL de redirección contenga '/espace_utilisateur'

def test_login_success_admin(client):
    response = client.post('/se_connecter', data={
        'inputEmail': 'adminuser@hotmail.com',
        'inputPass': 'Adminuser1#'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert '/espace_administrateur' in response.location  # Verifica que la URL de redirección contenga '/espace_administrateur'


def test_login_user_not_exist(client):
    """Prueba que se maneje correctamente cuando el usuario no existe."""
    response = client.post('/se_connecter', data={
        'inputEmail': 'noexist@example.com',
        'inputPass': 'fakepassword'
    }, follow_redirects=True)

    assert response.status_code == 200

    html_content = response.data.decode()
    expected_error_msg = "L&#39;adresse e-mail ou le mot de passe est incorrect."
    assert expected_error_msg in html_content, f"Expected error message not found! Received content: {html_content}"