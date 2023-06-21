
"""

from flask import Flask, render_template, redirect, session, request, url_for
from flask_bootstrap import Bootstrap
from datetime import datetime
import json
import mysql.connector
from dotenv import load_dotenv
import os




app = Flask(__name__)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True

app.secret_key='Pocholo123456'



bootstrap = Bootstrap(app)

load_dotenv()

db_config = {
    'user' : 'Vpinto',
    'password': os.getenv('DB_PASSSWORD'),
    'host': 'localhost',
    'database' : 'bdsuperbowl',
    'auth_plugin' : 'mysql_native_password'
}


def connect_to_database():
    cnx = mysql.connector.connect(**db_config)
    return cnx




class Matchs:
    def __init__(self, equipe1, equipe2, jour, debut, fin, statut, score, meteo, joueurs, cote1, cote2, commentaires):
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.jour = jour
        self.debut = debut
        self.fin = fin
        self.statut = statut
        self.score = score
        self.meteo = meteo
        self.joueurs = joueurs
        self.cote1 = cote1
        self.cote2 = cote2
        self.commentaires = commentaires


def obtenir_matchs():
     matchs = [
        Matchs('Kansas City Chiefs', 'Dallas Cowboys', '23/05', '09:00', '11:00', 'En cours','4-2', 'soleil','pepe', '500$', '200$' , 'el mejor jugador'),
        Matchs('New England Patriots', 'Green Bay Packers', '24/05', '08:00', '10:00', 'Terminé','0-3', 'pluie', 'batista', '400$','200$', 'que rule'),
        Matchs('Pittsburgh Steelers', 'San Francisco 49ers', '29/05', '10:00', '12:00', 'À venir','', 'horage', 'ronaldinho', '2000$','200$', 'El gaucho')
        ]
     return matchs

@app.route('/')

def index():
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y")
    return render_template('index.html', current_date=formatted_date)

@app.route('/visualiser_matchs')
def visualiser_matchs():
    matchs = obtenir_matchs()
    return render_template('visualiser_matchs.html', matchs = matchs)


@app.route('/store_in_session', methods=['POST'])
def store_in_session():
    session['equipe1'] = request.form.get('equipe1')
    session['equipe2'] = request.form.get('equipe2')
    session['cote1'] = request.form.get('cote1')
    session['cote2'] = request.form.get('cote2')
    return redirect(url_for('miser'))

@app.route('/miser')
def miser():
    equipe1 = session.get('equipe1')
    equipe2 = session.get('equipe2')
    cote1 = session.get('cote1')
    cote2 = session.get('cote2')
    return render_template('miser.html', equipe1=equipe1, equipe2=equipe2, cote1=cote1, cote2=cote2)


@app.route('/parier')
def parier():
    matchs = obtenir_matchs()
    return render_template('parier.html', matchs=matchs)

@app.route('/miser_sur_la_selection', methods=['POST'])
def miser_sur_la_selection():
   
   
    donnees_selectionnees = request.form.get('donnees_selectionnees')
    
    # JSON a objet Python
    matchs_selectionnes = json.loads(donnees_selectionnees)

    equipe1 = request.form.get('equipe1')
    equipe2 = request.form.get('equipe2')
    cote1 = request.form.get('cote1')
    cote2 = request.form.get('cote2')


   
    return render_template('miser_sur_la_selection.html', matchs_selectionnes=matchs_selectionnes, equipe1=equipe1, equipe2=equipe2, cote1=cote1,cote2=cote2)

@app.route('/se_connecter')
def se_connecter():
    return render_template('se_connecter.html')

@app.route('/mot_de_passe_oublie')
def mot_de_passe_oublie():
    return render_template("mot_de_passe_oublie.html")

@app.route('/creation_compte')
def creation_compte():
    return render_template("creation_compte.html")


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


"""
from flask import Flask, render_template, redirect, session, request, url_for

from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_mail import Mail, Message
import secrets
import json
from flaskext.mysql import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = 'Pocholo123456'
load_dotenv()

app.config['SECRET_KEY'] = 'Pocholo123456'
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'staniaprojets@gmail.com'
app.config['MAIL_PASSWORD'] = 'Stania1234#'
app.config['MAIL_DEFAULT_SENDER'] = 'staniaprojets@gmail.com'

mail = Mail(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'PEPE'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PEPE'
app.config['MYSQL_DATABASE_DB'] = 'bdsuperbowl'
mysql.init_app(app)

bootstrap = Bootstrap(app)


class Matchs:
    def __init__(self, equipe1, equipe2, jour, debut, fin, statut, score, meteo, joueurs, cote1, cote2, commentaires):
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.jour = jour
        self.debut = debut
        self.fin = fin
        self.statut = statut
        self.score = score
        self.meteo = meteo
        self.joueurs = joueurs
        self.cote1 = cote1
        self.cote2 = cote2
        self.commentaires = commentaires


def insert_matchs(matchs):
    conn = mysql.connect()
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO matchs (equipe1, equipe2, jour, debut, fin, statut, score, meteo, joueurs, cote1, cote2, commentaires)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    for match in matchs:
        data = (
            match.equipe1, match.equipe2, match.jour, match.debut, match.fin,
            match.statut, match.score, match.meteo, match.joueurs, match.cote1,
            match.cote2, match.commentaires
        )
        cursor.execute(insert_query, data)

    conn.commit()

    cursor.close()
    conn.close()


def obtenir_matchs_from_database():
    conn = mysql.connect()
    cursor = conn.cursor()

    select_query = "SELECT equipe1, equipe2, jour, debut, fin, statut, score, meteo, joueurs, cote1, cote2, commentaires FROM matchs"
    cursor.execute(select_query)
    matchs_data = cursor.fetchall()

    matchs = []
    for match_data in matchs_data:
        match = Matchs(*match_data)
        matchs.append(match)

    cursor.close()
    conn.close()

    return matchs


@app.route('/')
def index():
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y")
    return render_template('index.html', current_date=formatted_date)


@app.route('/visualiser_matchs')
def visualiser_matchs():
    matchs = obtenir_matchs_from_database()
    return render_template('visualiser_matchs.html', matchs=matchs)


@app.route('/store_in_session', methods=['POST'])
def store_in_session():
    session['equipe1'] = request.form.get('equipe1')
    session['equipe2'] = request.form.get('equipe2')
    session['cote1'] = request.form.get('cote1')
    session['cote2'] = request.form.get('cote2')
    return redirect(url_for('miser'))


@app.route('/miser')
def miser():
    equipe1 = session.get('equipe1')
    equipe2 = session.get('equipe2')
    cote1 = session.get('cote1')
    cote2 = session.get('cote2')
    return render_template('miser.html', equipe1=equipe1, equipe2=equipe2, cote1=cote1, cote2=cote2)


@app.route('/parier')
def parier():
    matchs = obtenir_matchs_from_database()
    return render_template('parier.html', matchs=matchs)


@app.route('/miser_sur_la_selection', methods=['POST'])
def miser_sur_la_selection():
    donnees_selectionnees = request.form.get('donnees_selectionnees')
    # JSON a objeto Python
    matchs_selectionnes = json.loads(donnees_selectionnees)
    equipe1 = request.form.get('equipe1')
    equipe2 = request.form.get('equipe2')
    cote1 = request.form.get('cote1')
    cote2 = request.form.get('cote2')
    return render_template('miser_sur_la_selection.html', matchs_selectionnes=matchs_selectionnes, equipe1=equipe1, equipe2=equipe2, cote1=cote1, cote2=cote2)



@app.route('/creation_compte', methods=['POST'])
def creation_compte_form():
    # Obtener los datos del formulario
    nom = request.form.get('inputNom')
    prenom = request.form.get('inputPrenom')
    email = request.form.get('inputEmail')
    mot_de_passe = request.form.get('inputPass')

    # token de validation
    token = secrets.token_hex(16)

    # Guardar los datos en la base de datos
    conn = mysql.connect()
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO users (nom, prenom, email, mot_de_passe)
        VALUES (%s, %s, %s, %s)
    '''
    data = (nom, prenom, email, mot_de_passe)
    cursor.execute(insert_query, data)

    conn.commit()

    cursor.close()
    conn.close()

    # Envoi du mail de validation
    msg = Message('Confirmez votre compte', sender='staniaprojets@gmail.com', recipients=[email])
    msg.body = f'Bonjour {prenom}, s’il vous plaît cliquez sur le lien pour valider votre compte: {request.url_root}confirmer/{token}'
    mail.send(msg)

    # Redireccionar a otra página o mostrar un mensaje de éxito
    return redirect(url_for('reussite_creation_compte'))

@app.route('/confirmer/<token>')
def confirmer_compte(token):
    conn = mysql.connect()
    cursor = conn.cursor()

    update_query = '''
        UPDATE users SET confirmed = 1 WHERE token = %s
    '''
    cursor.execute(update_query, (token,))

    conn.commit()

    cursor.close()
    conn.close()

    # Redireccionar a una página de confirmación exitosa o mostrar un mensaje
    return 'Votre compte a été valide. Bienvenue!'

@app.route('/reussite_creation_compte')
def reussite_creation_compte():
    return render_template("reussite_creation_compte.html")

@app.route('/creation_compte')
def creation_compte():
    return render_template("creation_compte.html")


@app.route('/se_connecter', methods=['POST'])
def se_connecter_validation():
    email = request.form.get('inputEmail')
    mot_de_passe = request.form.get('inputPass')

    conn = mysql.connect()
    curseur = conn.cursor()

    requete_select = "SELECT * FROM users WHERE email = %s AND mot_de_passe = %s"
    curseur.execute(requete_select, (email, mot_de_passe))
    utilisateur = curseur.fetchone()

    curseur.close()
    conn.close()

    if utilisateur:
        # Les identifiants sont valides
        session['utilisateur_id'] = utilisateur[0]  # Sauvegarder l'ID de l'utilisateur en session
        return redirect(url_for('espace_utilisateur'))
    else:
        # Les identifiants sont invalides
        erreur = 'Adresse e-mail ou mot de passe incorrect'
        return render_template('se_connecter.html', erreur=erreur)


@app.route('/se_connecter')
def se_connecter():
    return render_template('se_connecter.html')

@app.route('/espace_utilisateur')
def espace_utilisateur():
    return render_template('espace_utilisateur.html')


@app.route('/mot_de_passe_oublie')
def mot_de_passe_oublie():
    return render_template("mot_de_passe_oublie.html")




