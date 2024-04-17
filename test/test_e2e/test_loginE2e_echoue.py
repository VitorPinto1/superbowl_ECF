from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration du pilote pour utiliser Chrome
driver = webdriver.Chrome()

try:
    # Naviguer vers la page de connexion
    driver.get("http://127.0.0.1:5000/se_connecter")

    # Entrer l'adresse email
    email_input = driver.find_element(By.ID, "inputEmail")
    email_input.send_keys("testfail@hotmail.com")

    # Entrer le mot de passe
    password_input = driver.find_element(By.ID, "inputPass")
    password_input.send_keys("Testfail1#")

    # Soumettre le formulaire
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "erreurConnexion"))
    )


    print("Test de non connexion réussi!")
except Exception as e:
    print(f"Test échoué : {e} - L'erreur peut être liée à un problème de connexion ou à la non présence de l'élément.")
finally:
    driver.quit()
