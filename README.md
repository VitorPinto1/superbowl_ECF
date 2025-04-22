# superbowl_ECF

Prérequis

-	Visual Studio Code
-	Extension Python pour VS Code
-	Git
-	Python 3.9
-	Flask
-	Mailtrap
- MongoDB

1.	Installation et déploiement

Lancez VSCode et installez l’extension « Python » publiée par Microsoft. Après avoir créé le dossier. Ouvrez un terminal intégré dans VS Code pour faire le clonage du dépôt et exécuter les commandes suivantes :

	« git clone https://github.com/VitorPinto1/superbowl_ECF.git »
	« cd superbowl_ECF »

2. 	Configuration de l'environnement

Activez l'environnement virtuel Python dans le terminal :

	« source env/bin/activate »  # Sur Unix ou MacOS
	« env\Scripts\activate »    # Sur Windows

3. 	Lancement de l’application

Exécutez l’application avec Flask dans le teminal :

	« python app.py »
	« flask run »

4. 	Accéder à l’application

Ouvrez le navigateur et allez à :
	
 	http://127.0.0.1:5000/

Service de mail local

Pour visualiser les emails, ouvrez un navigateur et allez à :

	-https://mailtrap.io/home


Déploiement avec Docker

Prérequis :

- Docker Desktop installé

Lancer l'application avec Docker Compose

	« docker-compose up »

Construction manuelle 
Construire et lancer sans docker-compose :

	«	docker build -t vitorpinto500/superbowl:latest .
		docker run -it --rm -p 8080:5001 vitorpinto500/superbowl:latest

CI/CD à chaque git push sur main :

- L'image Docker est automatiquement construite avec GitHub Actions

- L'image est poussée sur DockerHub sous : vitorpinto500/apppython:latest

Auteur

Projet réalisé par Vitor Pinto Passionné par le développement et l'IA.