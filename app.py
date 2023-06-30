from flask import Flask, render_template, redirect, session, request, url_for
from flask_bootstrap import Bootstrap
from datetime import datetime
from decimal import Decimal
from flask_mail import Mail, Message
import secrets
import json
import random
import string
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

""""
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
"""

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

def generer_mot_de_passe(longueur):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(longueur))
    return mot_de_passe


@app.route('/')
def index():
  now = datetime.now()
  formatted_date = now.strftime("%d/%m/%Y")

  if 'id_utilisateur' in session:
    id_utilisateur = session['id_utilisateur']
    conn = mysql.connect()
    curseur = conn.cursor()

    select_query = "SELECT role FROM users WHERE id = %s"
    curseur.execute(select_query, (id_utilisateur,))
    role = curseur.fetchone()[0]
    curseur.close()
    conn.close()

    if role == 'admin':
      return render_template('index.html', current_date=formatted_date, voir_bouton_mon_espace=True, voir_bouton_se_connecter=False, voir_bouton_miser=True, user_admin = True)
    else:
      return render_template('index.html', current_date=formatted_date, voir_bouton_mon_espace=True, voir_bouton_se_connecter=False, voir_bouton_miser=True, user_admin = False)
    
  return render_template('index.html', current_date=formatted_date, voir_bouton_mon_espace=False, voir_bouton_se_connecter=True, voir_bouton_miser=False)



@app.route('/visualiser_matchs')
def visualiser_matchs():
    matchs = obtenir_matchs_from_database()
    voir_bouton_miser = False

    if 'id_utilisateur' in session:
        id_utilisateur = session['id_utilisateur']
        conn = mysql.connect()
        curseur = conn.cursor()

        select_query = "SELECT role FROM users WHERE id = %s"
        curseur.execute(select_query, (id_utilisateur,))
        role = curseur.fetchone()[0]
        curseur.close()
        conn.close()

        if role == 'user':
            voir_bouton_miser = True

    return render_template('visualiser_matchs.html', voir_bouton_miser=voir_bouton_miser, matchs=matchs)



@app.route('/store_in_session', methods=['POST'])
def store_in_session():
    session['equipe1'] = request.form.get('equipe1')
    session['equipe2'] = request.form.get('equipe2')
    session['cote1'] = request.form.get('cote1')
    session['cote2'] = request.form.get('cote2')
    session['mise1'] = request.form.get('mise1') 
    session['mise2'] = request.form.get('mise2')
    return redirect(url_for('miser'))


@app.route('/miser')
def miser():
    equipe1 = session.get('equipe1')
    equipe2 = session.get('equipe2')
    cote1 = session.get('cote1')
    cote2 = session.get('cote2')
    return render_template('miser.html', equipe1=equipe1, equipe2=equipe2, cote1=cote1, cote2=cote2)

@app.route('/form_miser', methods=['POST'])
def form_miser():
    mise1 = request.form.get('mise1')
    mise2 = request.form.get('mise2')
    resultat1 = request.form.get('resultat1')
    resultat2 = request.form.get('resultat2')
    equipe1 = session.get('equipe1')
    equipe2 = session.get('equipe2')
    cote1 = session.get('cote1')
    cote2 = session.get('cote2')
    utilisateur = session['id_utilisateur']

    conn = mysql.connect()
    cursor = conn.cursor()

    select_match_query = "SELECT id FROM matchs WHERE equipe1 = %s AND equipe2 = %s"
    cursor.execute(select_match_query, (equipe1, equipe2))
    match = cursor.fetchone()
    id_match = match[0]

    insert_query = '''
        INSERT INTO mises (mise1, mise2, resultat1, resultat2, equipe1, equipe2, cote1, cote2, id_utilisateur, id_match)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = (Decimal(mise1), Decimal(mise2), resultat1, resultat2, equipe1, equipe2, cote1, cote2, utilisateur, id_match)
    cursor.execute(insert_query, data)

    conn.commit()

    cursor.close()
    conn.close()

    """return render_template('espace_utilisateur.html', cote1=cote1, cote2=cote2, equipe1=equipe1, equipe2=equipe2, mise1=mise1, mise2=mise2, resultat1=resultat1, resultat2=resultat2, utilisateur=utilisateur)
    """
    return redirect('/espace_utilisateur')

@app.route('/mise/<int:mise_id>/modifier', methods=['GET'])
def modifier_mise(mise_id):
    conn = mysql.connect()
    curseur = conn.cursor()

    requete_select = "SELECT mises.*, matchs.equipe1, matchs.equipe2 FROM mises INNER JOIN matchs ON mises.id_match = matchs.id WHERE mises.id = %s"
    curseur.execute(requete_select, (mise_id,))
    mise = curseur.fetchone()

    if mise:
        equipe1 = mise[11]  # Obtener el nombre del equipo 1 de la mise desde la columna 'equipe1' de la tabla 'matchs'
        equipe2 = mise[12]  # Obtener el nombre del equipo 2 de la mise desde la columna 'equipe2' de la tabla 'matchs'

        curseur.close()
        conn.close()

        cote1 = mise[7]  # Obtener el valor de cote1 de la mise
        cote2 = mise[8]  # Obtener el valor de cote2 de la mise

        # Renderizar el template antes de eliminar la apuesta antigua
        render_avant_supprimer = render_template('miser.html', equipe1=equipe1, equipe2=equipe2, cote1=cote1, cote2=cote2)
        
        # Agregar lógica para eliminar la apuesta antigua
        conn = mysql.connect()
        curseur = conn.cursor()
        requete_delete = "DELETE FROM mises WHERE id = %s"
        curseur.execute(requete_delete, (mise_id,))
        conn.commit()
        curseur.close()
        conn.close()
        
        return render_avant_supprimer
    else:
        # Mise no encontrada
        return "Mise no encontrada"


@app.route('/mise/<int:mise_id>/supprimer', methods=['GET'])
def supprimer_mise(mise_id):
    conn = mysql.connect()
    curseur = conn.cursor()

    requete_supprimer = "DELETE FROM mises WHERE id = %s"
    curseur.execute(requete_supprimer, (mise_id,))
    conn.commit()

    curseur.close()
    conn.close()

    id_utilisateur = session['id_utilisateur']
    conn = mysql.connect()
    curseur = conn.cursor()
    
    select_utilisateur_query = "SELECT * FROM users WHERE id = %s"
    curseur.execute(select_utilisateur_query, (id_utilisateur,))
    utilisateur = curseur.fetchone()

    # Obtener las apuestas del usuario
    select_mises_query = '''
        SELECT mises.id, matchs.equipe1, matchs.equipe2, matchs.jour, matchs.debut, matchs.fin, mises.mise1, mises.mise2, mises.resultat1, mises.resultat2, matchs.statut
        FROM mises
        JOIN matchs ON mises.id_match = matchs.id
        WHERE mises.id_utilisateur = %s
    '''
    curseur.execute(select_mises_query, (id_utilisateur,))
    mises = curseur.fetchall()

    curseur.close()
    conn.close()

    return render_template('espace_utilisateur.html', utilisateur=utilisateur, mises=mises, active_tab='historique')





@app.route('/parier')
def parier():
  matchs = obtenir_matchs_from_database()

  voir_bouton_miser_selection = False

  if 'id_utilisateur' in session:
    id_utilisateur = session['id_utilisateur']
    conn = mysql.connect()
    curseur = conn.cursor()

    select_query = "SELECT role FROM users WHERE id = %s"
    curseur.execute(select_query, (id_utilisateur,))
    role = curseur.fetchone()[0]
    curseur.close()
    conn.close()

    if role == 'user':
        voir_bouton_miser_selection = True

  return render_template('parier.html', voir_bouton_miser_selection=voir_bouton_miser_selection, matchs=matchs)


@app.route('/miser_sur_la_selection', methods=['POST'])
def miser_sur_la_selection():
    donnees_selectionnees = request.form.get('donnees_selectionnees')
    # JSON a objeto Python
    matchs_selectionnes = json.loads(donnees_selectionnees)
    equipe1 = request.form.get('equipe1')
    equipe2 = request.form.get('equipe2')
    cote1 = request.form.get('cote1')
    cote2 = request.form.get('cote2')

    session['miser_sur_la_selection'] = matchs_selectionnes

    return render_template('miser_sur_la_selection.html', matchs_selectionnes=matchs_selectionnes, equipe1=equipe1, equipe2=equipe2, cote1=cote1, cote2=cote2)

@app.route('/form_miser_selection', methods=['POST'])
def form_miser_selection():
    mise1 = request.form.get('mise_equipe1')
    mise2 = request.form.get('mise_equipe2')
    
    matchs_selectionnes = session.get('miser_sur_la_selection')

    conn = mysql.connect()
    cursor = conn.cursor()

    
    for index, match in enumerate(matchs_selectionnes):
        equipe1 = match['equipe1']
        equipe2 = match['equipe2']
        cote1 = match['cote1']
        cote2 = match['cote2']
        utilisateur = session['id_utilisateur']

        select_match_query = "SELECT id FROM matchs WHERE equipe1 = %s AND equipe2 = %s"
        cursor.execute(select_match_query, (equipe1, equipe2))
        match = cursor.fetchone()
        if match:
            id_match = match[0]

            resultat1 = request.form.get('resultat1_{}'.format(index + 1))
            resultat2 = request.form.get('resultat2_{}'.format(index + 1))


            insert_query = '''
                INSERT INTO mises (mise1, mise2, resultat1, resultat2, equipe1, equipe2, cote1, cote2, id_utilisateur, id_match)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            data = (Decimal(mise1), Decimal(mise2), resultat1, resultat2, equipe1, equipe2, cote1, cote2, utilisateur, id_match)
            cursor.execute(insert_query, data)

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/espace_utilisateur')

@app.route('/creation_compte', methods=['POST'])
def creation_compte_form():
    
    nom = request.form.get('inputNom')
    prenom = request.form.get('inputPrenom')
    email = request.form.get('inputEmail')
    mot_de_passe = request.form.get('inputPass')

    # token de validation
    token = secrets.token_hex(16)

    
    conn = mysql.connect()
    cursor = conn.cursor()

    
    # Vérification pour savoir si email existe déjà dans la base de données
    check_query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(check_query, (email,))
    utilisateur = cursor.fetchone()

    
    
    if utilisateur:
        # Si l'email est déjà utilisé, rediriger ou afficher un message d'erreur
        erreur = "Email déjà utilisé"
        return render_template ('creation_compte.html', erreur=erreur)
    else:
        # Créer un token de validation
        token = secrets.token_hex(16)

        # Insérer le nouvel utilisateur dans la base de données
        insert_query = '''
            INSERT INTO users (nom, prenom, email, mot_de_passe, token)
            VALUES (%s, %s, %s, %s, %s)
        '''
        data = (nom, prenom, email, mot_de_passe, token)
        cursor.execute(insert_query, data)

        conn.commit()

        # Envoyer l'email de validation
        msg = Message('Confirmez votre compte', sender='staniaprojets@gmail.com', recipients=[email])
        msg.body = f'Bonjour {prenom}, s’il vous plaît cliquez sur le lien pour valider votre compte: {request.url_root}confirmer/{token}'
        mail.send(msg)

    cursor.close()
    conn.close()

    # Rediriger vers une autre page ou afficher un message de succès
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
    return render_template('se_connecter.html')

@app.route('/reussite_creation_compte')
def reussite_creation_compte():
    return render_template('reussite_creation_compte.html')

@app.route('/creation_compte')
def creation_compte():
    return render_template('creation_compte.html')

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
        if  utilisateur[6] == 1:  # En supposant que 'confirmed' soit la septieme colonne dans la table 'users'
         
            # Les identifiants sont corrects
            session['id_utilisateur'] = utilisateur[0]  # Enregistrer l'ID de l'utilisateur en session
            if utilisateur[7] == 'admin':  # En supposant que 'role' soit la huitième colonne dans la table 'users'
                return redirect(url_for('espace_administrateur'))
            else:
                return redirect(url_for('espace_utilisateur'))
        else:
            # Les identifiants sont corrects, mais l'utilisateur n'a pas encore confirmé son compte.
            erreur = "Veuillez confirmer votre compte avant de vous connecter."
            return render_template('se_connecter.html', erreur=erreur)
    else:
        # Les identifiants sont incorrects
        erreur = "L'adresse e-mail ou le mot de passe est incorrect."
        return render_template('se_connecter.html', erreur=erreur)

@app.route('/se_connecter')
def se_connecter():
    if 'id_utilisateur' in session:
        id_utilisateur = session['id_utilisateur']
        conn = mysql.connect()
        curseur = conn.cursor()

        select_query = "SELECT role FROM users WHERE id = %s"
        curseur.execute(select_query, (id_utilisateur,))
        role = curseur.fetchone()[0]
        curseur.close()
        conn.close()

        if role == 'admin':
            return redirect(url_for('espace_administrateur'))
        else:
            return redirect(url_for('espace_utilisateur'))
    else:
        return render_template('se_connecter.html')


@app.route('/mot_de_passe_oublie', methods=['GET', 'POST'])
def mot_de_passe_oublie_form():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['inputEmail']

        # Générer un nouveau mot de passe
        nouveau_mot_de_passe = generer_mot_de_passe(8) 


        # Mettre à jour le mot de passe dans la base de données
        conn = mysql.connect()
        cursor = conn.cursor()

        update_query = '''
            UPDATE users SET mot_de_passe = %s WHERE email = %s
        '''
        cursor.execute(update_query, (nouveau_mot_de_passe, email))

        conn.commit()

        cursor.close()
        conn.close()

        # Envoyer l'email
        msg = Message("Récupération de mot de passe",
                      sender='staniaprojets@gmail.com',
                      recipients=[email])
        msg.body = "Bonjour " + nom + ",\n\nVotre nouveau mot de passe est : " + nouveau_mot_de_passe + "\n\nMerci."

        mail.send(msg)

        return "L'email a été envoyé avec succès."

    return render_template('mot_de_passe_oublie.html')


@app.route('/mot_de_passe_oublie', methods=['GET'])
def mot_de_passe_oublie():
    return render_template("mot_de_passe_oublie.html")

@app.route('/espace_utilisateur', methods=['GET'])
def espace_utilisateur():
    # Obtenir l'ID de l'utilisateur de la session
    id_utilisateur = session['id_utilisateur']
    

    # Connecter à la base de données
    conn = mysql.connect()
    cursor = conn.cursor()

    # Sélectionner l'utilisateur par son ID
    select_query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(select_query, (id_utilisateur,))
    utilisateur = cursor.fetchone()


    # Sélectionner les paris de l'utilisateur
    select_mises_query = '''
        SELECT mises.id, matchs.equipe1, matchs.equipe2, matchs.jour, matchs.debut, matchs.fin, mises.mise1, mises.mise2, mises.resultat1, mises.resultat2, matchs.statut
        FROM mises
        JOIN matchs ON mises.id_match = matchs.id
        WHERE mises.id_utilisateur = %s
    '''
    cursor.execute(select_mises_query, (id_utilisateur,))
    mises = cursor.fetchall()

    cursor.close()
    conn.close()

  
    # Renvoyer le modèle avec les informations utilisateur
    return render_template('espace_utilisateur.html', utilisateur = utilisateur, mises=mises)

@app.route('/espace_administrateur')
def espace_administrateur():
    return render_template('espace_administrateur.html')

# déconnexion du compte lors de la fermeture du web
@app.route('/deconnecter_utilisateur', methods=['POST'])
def deconnecter_utilisateur():
    session.pop('id_utilisateur', None)  # Eliminar la clave 'id_utilisateur' de la sesión
    return '', 204  # Devolver una respuesta vacía con código de estado 204 (sin contenido)

@app.route('/deconnexion_user_bouton', methods=['POST'])
def deconnexion_user_bouton():
    session.pop('id_utilisateur', None)  # Eliminar la clave 'id_utilisateur' de la sesión
    return redirect(url_for('index'))

@app.route('/creation')
def creation():
    return render_template('creation.html')

@app.route('/planification')
def planification():
    return render_template('planification.html')