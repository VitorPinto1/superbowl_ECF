from flask import Flask, render_template, redirect, session, request, url_for, jsonify
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
from faker import Faker


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
    def __init__(self, equipe1, equipe2, jour, debut, fin, statut, score, meteo, cote1, cote2, commentaires, joueurs_equipe1, joueurs_equipe2):
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.jour = jour
        self.debut = debut
        self.fin = fin
        self.statut = statut
        self.score = score
        self.meteo = meteo
        self.cote1 = cote1
        self.cote2 = cote2
        self.commentaires = commentaires
        self.joueurs_equipe1 = joueurs_equipe1
        self.joueurs_equipe2 = joueurs_equipe2
        

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

    select_query = '''
    SELECT 
        m.equipe1, 
        m.equipe2, 
        m.jour, 
        m.debut, 
        m.fin, 
        m.statut, 
        m.score, 
        m.meteo,  
        m.cote1, 
        m.cote2, 
        m.commentaires,
        GROUP_CONCAT(DISTINCT CONCAT(j1.nom_joueur, ' ', j1.prenom_joueur, ' (#', j1.numero_tshirt, ')') ORDER BY j1.nom_joueur SEPARATOR ', ') AS joueurs_equipe1,
        GROUP_CONCAT(DISTINCT CONCAT(j2.nom_joueur, ' ', j2.prenom_joueur, ' (#', j2.numero_tshirt, ')') ORDER BY j2.nom_joueur SEPARATOR ', ') AS joueurs_equipe2
    FROM 
        matchs m
    LEFT JOIN 
        equipes e1 ON m.equipe1 = e1.nom_equipe
    LEFT JOIN 
        joueurs j1 ON e1.id = j1.equipe_id
    LEFT JOIN 
        equipes e2 ON m.equipe2 = e2.nom_equipe
    LEFT JOIN 
        joueurs j2 ON e2.id = j2.equipe_id
    GROUP BY 
        m.equipe1, m.equipe2, m.jour, m.debut, m.fin, m.statut, m.score, m.meteo, m.cote1, m.cote2, m.commentaires
    ORDER BY 
        CASE m.statut 
            WHEN 'En cours' THEN 1
            WHEN 'Terminé' THEN 2
            WHEN 'À venir' THEN 3
            ELSE 4
        END


    '''

    cursor.execute(select_query)
    matchs_data = cursor.fetchall()

    matchs = []
    for match_data in matchs_data:
        match = Matchs(*match_data)
        if match.fin is None:
            match.fin = ' - '
        if match.statut is None:
            match.statut = ' - '
        if match.score is None:
            match.score = ' - '
        if match.meteo is None:
            match.meteo = ' - '
        if match.commentaires is None:
            match.commentaires = ' - '

        matchs.append(match)

    cursor.close()
    conn.close()

    return matchs





def generer_mot_de_passe(longueur):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(longueur))
    return mot_de_passe

def generer_meteo_aleatoire():
    conditions = ["Ensoleillé", "Nuageux", "Pluvieux", "Venteux", "Neigeux"]
    temperature = random.randint(-10, 35)  # Température aléatoire entre -10 et 35 degrés
    condition = random.choice(conditions)
    meteo = f"{condition}, {temperature}°C"
    return meteo

fake = Faker()

def random_prenom(equipe_id, numero_joueurs = 11):
    joueurs_prenom = []
    for _ in range(numero_joueurs):
        nom_complet = fake.name()
        nom_parts = nom_complet.split(' ')
        nom_joueur = nom_parts[0]
        if len(nom_parts) > 1:
            prenom_joueur = ' '.join(nom_parts[1:])  # Resto del nombre (apellido)
        else:
            prenom_joueur = ''
        numero_tshirt = random.randint(1,99)
        joueurs_prenom.append((nom_joueur, prenom_joueur, numero_tshirt, equipe_id))
    return joueurs_prenom

def ajouter_joueurs(joueurs_prenom):
    conn = mysql.connect()
    cursor = conn.cursor()
    for joueur_prenom in joueurs_prenom:
        insert_query = "INSERT INTO joueurs (nom_joueur, prenom_joueur, numero_tshirt, equipe_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, joueur_prenom)

    conn.commit()
    cursor.close()
    conn.close()

def verifier_existence_joueurs(equipe_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM joueurs WHERE equipe_id = %s", (equipe_id,))
    (count,) = cursor.fetchone()
    cursor.close()
    conn.close()
    return count > 0

equipes_ids = list(range(1, 33))  # Reemplaza con los IDs reales de tus equipos

for equipe_id in equipes_ids:
    if not verifier_existence_joueurs(equipe_id):
        joueurs_prenom = random_prenom(equipe_id)
        ajouter_joueurs(joueurs_prenom)


@app.route('/')
def index():
  now = datetime.now()
  formatted_date = now.strftime("%d/%m/%Y")
  conn = mysql.connect()

    # Crear un cursor para ejecutar consultas
  cursor = conn.cursor()

  # Obtener la fecha actual
  cursor.execute("SELECT CURDATE()")
  current_date = cursor.fetchone()[0]

  # Obtener los partidos de la fecha actual
  cursor.execute("SELECT * FROM matchs WHERE jour = %s", (current_date,))
  matches = cursor.fetchall()

  # Cerrar el cursor y la conexión
  cursor.close()
  conn.close()


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
      return render_template('index.html', current_date=formatted_date, voir_bouton_mon_espace=True, voir_bouton_se_connecter=False, voir_bouton_miser=True, user_admin = True, matches=matches)
    else:
      return render_template('index.html', current_date=formatted_date, voir_bouton_mon_espace=True, voir_bouton_se_connecter=False, voir_bouton_miser=True, user_admin = False, matches=matches)
    
  return render_template('index.html', current_date=formatted_date, voir_bouton_mon_espace=False, voir_bouton_se_connecter=True, voir_bouton_miser=False, matches = matches)


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
    session['jour'] = request.form.get('jour')
    session['debut'] = request.form.get('debut')

    return redirect(url_for('miser'))


@app.route('/miser')
def miser():
    equipe1 = session.get('equipe1')
    equipe2 = session.get('equipe2')
    cote1 = session.get('cote1')
    cote2 = session.get('cote2')
    jour = session.get('jour')
    debut = session.get('debut')
    utilisateur = session['id_utilisateur']

    # Verificar si ya existe una apuesta para este usuario y partido
    conn = mysql.connect()
    cursor = conn.cursor()

    select_existing_bet_query = '''
        SELECT id FROM mises
        WHERE id_utilisateur = %s AND id_match IN (
            SELECT id FROM matchs WHERE equipe1 = %s AND equipe2 = %s AND jour = %s AND debut = %s
        )
    '''
    cursor.execute(select_existing_bet_query, (utilisateur, equipe1, equipe2, jour, debut))
    existing_bet = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('miser.html', equipe1=equipe1, equipe2=equipe2, cote1=cote1, cote2=cote2, jour=jour, debut=debut, existing_bet=existing_bet)


@app.route('/form_miser', methods=['POST'])
def form_miser():
    mise1 = request.form.get('mise1')
    mise2 = request.form.get('mise2')
    equipe1 = session.get('equipe1')
    equipe2 = session.get('equipe2')
    cote1 = session.get('cote1')
    cote2 = session.get('cote2')
    utilisateur = session['id_utilisateur']
    jour = session.get('jour') 
    debut = session.get('debut')
    
    datemise = datetime.now()

    conn = mysql.connect()
    cursor = conn.cursor()

    select_match_query = "SELECT id FROM matchs WHERE equipe1 = %s AND equipe2 = %s AND jour = %s AND debut = %s"
    cursor.execute(select_match_query, (equipe1, equipe2, jour, debut))
    match = cursor.fetchone()
    id_match = match[0]
    
    # Verificar si ya existe una apuesta para este usuario y partido
    select_existing_bet_query = '''
        SELECT id, equipe1, equipe2 FROM mises
        WHERE id_utilisateur = %s AND id_match = %s
    '''
    cursor.execute(select_existing_bet_query, (utilisateur, id_match))
    existing_bets = cursor.fetchall()

    if existing_bets:
        for existing_bet in existing_bets:
            # Eliminar la apuesta si el valor es 0 para el equipo 1
            if mise1 is not None and mise1.strip() == "0" and existing_bet[1] == equipe1:
                delete_query1 = '''
                    DELETE FROM mises
                    WHERE id = %s
                '''
                cursor.execute(delete_query1, (existing_bet[0],))
        
            # Actualizar la apuesta para el equipo 1
            elif existing_bet[1] == equipe1 and mise1 is not None and mise1.strip() != "":
                update_query1 = '''
                    UPDATE mises
                    SET mise1 = %s, resultat1 = %s
                    WHERE id = %s
                '''
                resultat1 = Decimal(mise1) * Decimal(cote1)
                data1 = (Decimal(mise1), resultat1, existing_bet[0])
                cursor.execute(update_query1, data1)

            # Eliminar la apuesta si el valor es 0 para el equipo 2
            if mise2 is not None and mise2.strip() == "0" and existing_bet[2] == equipe2:
                delete_query2 = '''
                    DELETE FROM mises
                    WHERE id = %s
                '''
                cursor.execute(delete_query2, (existing_bet[0],))
        
            # Actualizar la apuesta para el equipo 2
            elif existing_bet[2] == equipe2 and mise2 is not None and mise2.strip() != "":
                update_query2 = '''
                    UPDATE mises
                    SET mise2 = %s, resultat2 = %s
                    WHERE id = %s
                '''
                resultat2 = Decimal(mise2) * Decimal(cote2)
                data2 = (Decimal(mise2), resultat2, existing_bet[0])
                cursor.execute(update_query2, data2)

        conn.commit()

    

    else:
        # Si no existe una apuesta, insertar una nueva
        if mise1 is not None and mise1.strip() != "":
            insert_query1 = '''
                INSERT INTO mises (mise1, resultat1, equipe1, cote1, id_utilisateur, id_match, datemise)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            resultat1 = Decimal(mise1) * Decimal(cote1)
            data1 = (Decimal(mise1), resultat1, equipe1, cote1, utilisateur, id_match, datemise)
            cursor.execute(insert_query1, data1)

        if mise2 is not None and mise2.strip() != "":
            insert_query2 = '''
                INSERT INTO mises (mise2, resultat2, equipe2, cote2, id_utilisateur, id_match, datemise)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            resultat2 = Decimal(mise2) * Decimal(cote2)
            data2 = (Decimal(mise2), resultat2, equipe2, cote2, utilisateur, id_match, datemise)
            cursor.execute(insert_query2, data2)

        conn.commit()

    cursor.close()
    conn.close()

    return redirect('/espace_utilisateur')

@app.route('/mise/<int:mise_id>/modifier', methods=['GET'])
def modifier_mise(mise_id):
    conn = mysql.connect()
    curseur = conn.cursor()

    requete_select = "SELECT mises.*, matchs.equipe1, matchs.equipe2, matchs.cote1, matchs.cote2 FROM mises INNER JOIN matchs ON mises.id_match = matchs.id WHERE mises.id = %s"
    curseur.execute(requete_select, (mise_id,))
    mise = curseur.fetchone()

    if mise:
        equipe1 = mise[11]  # Obtener el nombre del equipo 1 de la mise
        equipe2 = mise[12]  # Obtener el nombre del equipo 2 de la mise
        cote1 = mise[13]      # Obtener el valor de cote1 de la mise
        cote2 = mise[14] 
        curseur.close()
        conn.close()

        

       

        # Agregar lógica para eliminar la apuesta antigua
        conn = mysql.connect()
        curseur = conn.cursor()
        requete_delete = "DELETE FROM mises WHERE id = %s"
        curseur.execute(requete_delete, (mise_id,))
        conn.commit()
        curseur.close()
        conn.close()
        
        # Renderizar el template después de eliminar la apuesta antigua
        return render_template('miser.html', equipe1=equipe1, equipe2=equipe2, cote1=cote1, cote2=cote2)
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
    jour = request.form.get('jour')

    session['miser_sur_la_selection'] = matchs_selectionnes

    return render_template('miser_sur_la_selection.html', matchs_selectionnes=matchs_selectionnes, equipe1=equipe1, equipe2=equipe2, cote1=cote1, cote2=cote2, jour=jour)

@app.route('/form_miser_selection', methods=['POST'])
def form_miser_selection():
    matchs_selectionnes = session.get('miser_sur_la_selection')
    
    conn = mysql.connect()
    cursor = conn.cursor()

    for index, match in enumerate(matchs_selectionnes):
        mise1 = request.form.get('mise_equipe1_{}'.format(index + 1))
        mise2 = request.form.get('mise_equipe2_{}'.format(index + 1))

        if mise1 is None:
            mise1 = '0'
        if mise2 is None:
            mise2 = '0'

        # Convertir los valores en Decimal
        mise1_decimal = Decimal(mise1)
        mise2_decimal = Decimal(mise2)

        equipe1 = match['equipe1']
        equipe2 = match['equipe2']
        cote1 = match['cote1']
        cote2 = match['cote2']
        jour = match['jour']
        utilisateur = session['id_utilisateur']
        datemise = datetime.now()
        

        select_match_query = "SELECT id FROM matchs WHERE equipe1 = %s AND equipe2 = %s AND jour = %s"
        cursor.execute(select_match_query, (equipe1, equipe2, jour))
        match = cursor.fetchone()
        if match:
            id_match = match[0]

            resultat1 = request.form.get('resultat1_{}'.format(index + 1))
            resultat2 = request.form.get('resultat2_{}'.format(index + 1))

            insert_query1 = '''
                INSERT INTO mises (mise1, resultat1, equipe1, cote1, id_utilisateur, id_match, datemise)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            data1 = (mise1_decimal, resultat1, equipe1, cote1, utilisateur, id_match, datemise)
            cursor.execute(insert_query1, data1)

            # Insertar la mise para el equipo 2
            insert_query2 = '''
                INSERT INTO mises (mise2, resultat2, equipe2, cote2, id_utilisateur, id_match, datemise)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            data2 = (mise2_decimal, resultat2, equipe2, cote2, utilisateur, id_match, datemise)
            cursor.execute(insert_query2, data2)

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
        SELECT mises.id, matchs.equipe1, matchs.equipe2, matchs.jour, matchs.debut, matchs.fin, mises.mise1, mises.mise2, mises.resultat1, mises.resultat2, matchs.statut, matchs.vainqueur, mises.equipe1, mises.equipe2
        FROM mises
        JOIN matchs ON mises.id_match = matchs.id
        WHERE mises.id_utilisateur = %s 
        ORDER BY 
            CASE matchs.statut 
                WHEN 'En cours' THEN 1
                WHEN 'Terminé' THEN 2
                WHEN 'À venir' THEN 3
                ELSE 4
            END
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

@app.route('/creation', methods=['POST'])
def creation_form():
    nom_equipe = request.form.get('nom_equipe')
    pays_appartenance = request.form.get('pays_appartenance')

    conn = mysql.connect()
    cursor = conn.cursor()

    # Verificar si el equipo ya existe en la base de datos
    check_query = "SELECT * FROM equipes WHERE nom_equipe = %s"
    cursor.execute(check_query, (nom_equipe,))
    equipe_deja_utilise = cursor.fetchone()

    if equipe_deja_utilise:
        # Si el equipo ya existe, mostrar un mensaje de error
        erreur = "Équipe déjà créée"
        return render_template('creation.html', erreur=erreur)
    else:
        # Insertar el equipo en la tabla "equipes"
        insert_equipe_query = "INSERT INTO equipes (nom_equipe, pays_appartenance) VALUES (%s, %s)"
        equipe_data = (nom_equipe, pays_appartenance)
        cursor.execute(insert_equipe_query, equipe_data)
        equipe_id = cursor.lastrowid

        joueurs = []
        for i in range(1, 12):
            nom_joueur = request.form.get(f'nom_joueur_{i}')
            prenom_joueur = request.form.get(f'prenom_joueur_{i}')
            numero_tshirt = request.form.get(f'numero_tshirt_{i}')
            if nom_joueur and prenom_joueur and numero_tshirt:
                joueur_data = (nom_joueur, prenom_joueur, numero_tshirt, equipe_id)
                joueurs.append(joueur_data)

        if joueurs:
            insert_joueur_query = "INSERT INTO joueurs (nom_joueur, prenom_joueur, numero_tshirt, equipe_id) VALUES (%s, %s, %s, %s)"
            cursor.executemany(insert_joueur_query, joueurs)

        conn.commit()

    cursor.close()
    conn.close()

    # Redirigir a otra página o mostrar un mensaje de éxito
    return redirect(url_for('espace_administrateur'))

@app.route('/planification', methods=['GET', 'POST'])

def planification_form():
    error_message = None
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT nom_equipe FROM equipes")
    original_equipes = [equipe[0] for equipe in cursor.fetchall()]
    conn.close()
    if request.method == 'POST':
        # Obtenir data form
        equipe1 = request.form['equipe1']
        equipe2 = request.form['equipe2']
        jour = datetime.strptime(request.form['jour'], '%Y-%m-%d').date()
        debut = request.form['debut']
        cote1 = request.form['cote1']
        cote2 = request.form['cote2']

        statut = "À venir"
        
        meteo = generer_meteo_aleatoire()
    

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM matchs WHERE equipe1 = %s AND equipe2 = %s AND jour = %s",
                       (equipe1, equipe2, jour))
        existing_match = cursor.fetchone()
        conn.close()

        if existing_match:
            error_message = "Il y a déjà un match avec les mêmes équipes et la même date."
            return render_template('planification.html', equipes=original_equipes, error_message=error_message)
        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO matchs (equipe1, equipe2, jour, debut,cote1, cote2, statut, meteo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (equipe1, equipe2, jour, debut, cote1, cote2, statut, meteo))
        conn.commit()
        conn.close()

        return redirect('/planification')
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT nom_equipe FROM equipes")
    equipes = [equipe[0] for equipe in cursor.fetchall()]
    conn.close()





    return render_template('planification.html', equipes = equipes)



@app.route('/planification')
def planification():
    return render_template('planification.html')