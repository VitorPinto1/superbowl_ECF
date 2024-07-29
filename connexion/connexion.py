from api.config import *


connexion_bp = Blueprint('connexion', __name__, template_folder='templates')



def generer_mot_de_passe(longueur):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    mot_de_passe = ''.join(random.choice(caracteres) for _ in range(longueur))
    return mot_de_passe


@connexion_bp.context_processor
def inject_user_info():
    from api.app import mysql
    user_info = {
        'user_admin': False
    }

    if 'id_utilisateur' in session:
        id_utilisateur = session['id_utilisateur']
        conn = mysql.connect()
        cursor = conn.cursor()

        # Obtenir le rôle de l'utilisateur de la base de données
        cursor.execute("SELECT role FROM users WHERE id = %s", (id_utilisateur,))
        result = cursor.fetchone()
        
        if result is not None:
            role = result[0]
            user_info['user_admin'] = role == 'admin'

        cursor.close()
        conn.close()
        

    return user_info




@connexion_bp.route('/creation_compte', methods=['POST'])
def creation_compte_form():
    from api.app import mysql, mail
    nom = request.form.get('inputNom')
    prenom = request.form.get('inputPrenom')
    email = request.form.get('inputEmail')
    mot_de_passe = request.form.get('inputPass')
    # Hash password
    mot_de_passe_hashe = generate_password_hash(mot_de_passe)
    # token 
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
        return render_template('creation_compte.html', erreur=erreur)
    else:
        # Insérer le nouvel utilisateur dans la base de données
        insert_query = '''
            INSERT INTO users (nom, prenom, email, mot_de_passe, token)
            VALUES (%s, %s, %s, %s, %s)
        '''
        data = (nom, prenom, email, mot_de_passe_hashe, token)
        cursor.execute(insert_query, data)
        conn.commit()

        # Envoyer l'email de validation
        msg = Message('Confirmez votre compte', sender='mailtrap@superbowlstania.com', recipients=[email])
        msg.body = f'Bonjour {prenom}, s’il vous plaît cliquez sur le lien pour valider votre compte: {request.url_root}confirmer/{token}'
        mail.send(msg)

    cursor.close()
    conn.close()

    # Rediriger vers une autre page ou afficher un message de succès
    return redirect(url_for('connexion.reussite_creation_compte'))

@connexion_bp.route('/confirmer/<token>')
def confirmer_compte(token):
    from api.app import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    update_query = '''
        UPDATE users SET confirmed = 1 WHERE token = %s
    '''
    cursor.execute(update_query, (token,))
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('se_connecter.html')

@connexion_bp.route('/reussite_creation_compte')
def reussite_creation_compte():
    return render_template('reussite_creation_compte.html')

@connexion_bp.route('/creation_compte')
def creation_compte():
    return render_template('creation_compte.html')

@connexion_bp.route('/se_connecter', methods=['POST'])
def se_connecter_validation():
    from api.app import mysql
    email = request.form.get('inputEmail')
    mot_de_passe = request.form.get('inputPass')
    conn = mysql.connect()
    curseur = conn.cursor()
    requete_select = "SELECT * FROM users WHERE email = %s"
    curseur.execute(requete_select, (email,))
    utilisateur = curseur.fetchone()
    curseur.close()
    conn.close()

    # Vérifier si l'utilisateur existe et comparer le mot de passe haché
    if utilisateur:
        mot_de_passe_hashe = utilisateur[4] 
        if check_password_hash(mot_de_passe_hashe, mot_de_passe):
            # Vérifier si l'utilisateur a confirmé son compte
            if utilisateur[6] == 1:  
                session['id_utilisateur'] = utilisateur[0]  # Enregistre l'identifiant de l'utilisateur dans la session
                if utilisateur[7] == 'admin': 
                    return redirect(url_for('admin.espace_administrateur'))
                else:
                    return redirect(url_for('user.espace_utilisateur'))
            else:
                erreur = "Veuillez confirmer votre compte avant de vous connecter."
                return render_template('se_connecter.html', erreur=erreur)
        else:
            erreur = "L'adresse e-mail ou le mot de passe est incorrect."
            return render_template('se_connecter.html', erreur=erreur)
    else:
        erreur = "L'adresse e-mail ou le mot de passe est incorrect."
        return render_template('se_connecter.html', erreur=erreur)

@connexion_bp.route('/se_connecter')
def se_connecter():
    from api.app import mysql
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
            return redirect(url_for('admin.espace_administrateur'))
        else:
            return redirect(url_for('user.espace_utilisateur'))
    else:
        return render_template('se_connecter.html')


@connexion_bp.route('/mot_de_passe_oublie', methods=['GET', 'POST'])
def mot_de_passe_oublie_form():
    from api.app import mysql, mail
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['inputEmail']
        # Générer un nouveau mot de passe
        nouveau_mot_de_passe = generer_mot_de_passe(8) 
        mot_de_passe_hashe = generate_password_hash(nouveau_mot_de_passe)
        # Mettre à jour le mot de passe dans la base de données
        conn = mysql.connect()
        cursor = conn.cursor()

        update_query = '''
            UPDATE users SET mot_de_passe = %s WHERE email = %s
        '''
        cursor.execute(update_query, (mot_de_passe_hashe, email))
        conn.commit()
        cursor.close()
        conn.close()

        # Envoyer l'email
        msg = Message("Récupération de mot de passe",
                      sender='mailtrap@superbowlstania.com',
                      recipients=[email])
        msg.body = "Bonjour " + nom + ",\n\nVotre nouveau mot de passe est : " + nouveau_mot_de_passe + "\n\nMerci."

        mail.send(msg)

        return "L'email a été envoyé avec succès."

    return render_template('mot_de_passe_oublie.html')


@connexion_bp.route('/mot_de_passe_oublie', methods=['GET'])
def mot_de_passe_oublie():
    return render_template("mot_de_passe_oublie.html")

@connexion_bp.route('/changer_mot_de_passe', methods=['GET', 'POST'])
def changer_mot_de_passe():
    from api.app import mysql
    if 'id_utilisateur' not in session:
        # Si l'utilisateur n'est pas connecté, rediriger vers la page de connexion
        return redirect(url_for('connexion.se_connecter'))

    if request.method == 'POST':
        nouveau_mot_de_passe = request.form.get('inputModificationMdp')
        id_utilisateur = session['id_utilisateur']

        # Se connecter à la base de données et mettre à jour le mot de passe
        conn = mysql.connect()
        cursor = conn.cursor()
        hashed_password = generate_password_hash(nouveau_mot_de_passe)
        update_query = "UPDATE users SET mot_de_passe = %s WHERE id = %s"
        cursor.execute(update_query, (hashed_password, id_utilisateur))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Votre mot de passe a été changé avec succès.', 'success')
        return redirect(url_for('user.espace_utilisateur'))

    return render_template('changer_mot_de_passe.html')

def admin_required(func):
    from api.app import mysql
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'id_utilisateur' in session:
            id_utilisateur = session['id_utilisateur']
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT role FROM users WHERE id = %s", (id_utilisateur,))
            result = cursor.fetchone()

            if result is not None:
                role = result[0]
                if role == 'admin':
                    return func(*args, **kwargs)

            cursor.close()
            conn.close()

        return redirect(url_for('index'))

    return decorated_function


@connexion_bp.route('/deconnecter_utilisateur', methods=['POST'])
def deconnecter_utilisateur():
    session.pop('id_utilisateur', None)  # Supprimer la clé 'id_utilisateur' de la session
    return '', 204  # Renvoyer une réponse vide avec le code 204 (pas de contenu)

@connexion_bp.route('/deconnexion_user_bouton', methods=['POST'])
def deconnexion_user_bouton():
    session.pop('id_utilisateur', None)  
    return redirect(url_for('index'))