from api.config import *
from flask import current_app


connexion_bp = Blueprint('connexion', __name__, template_folder='templates')

def generer_mot_de_passe(longueur):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(longueur))

@connexion_bp.route('/creation_compte', methods=['POST'])
def creation_compte_form():
    mysql = current_app.extensions['mysql']
    mail = current_app.extensions['mail']
    nom = request.form.get('inputNom')
    prenom = request.form.get('inputPrenom')
    email = request.form.get('inputEmail')
    mot_de_passe = request.form.get('inputPass')
    mot_de_passe_hashe = generate_password_hash(mot_de_passe)
    token = secrets.token_hex(16)
    conn = mysql.connect()
    cursor = conn.cursor()
    check_query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(check_query, (email,))
    utilisateur = cursor.fetchone()
    if utilisateur:
        erreur = "Email déjà utilisé"
        cursor.close()
        conn.close()
        return render_template('creation_compte.html', erreur=erreur)
    else:
        insert_query = '''
            INSERT INTO users (nom, prenom, email, mot_de_passe, token)
            VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (nom, prenom, email, mot_de_passe_hashe, token))
        conn.commit()
        cursor.close()
        conn.close()
        confirmation_url = url_for('connexion.confirmer_compte', token=token, _external=True)

        msg = Message(
            'Confirmez votre compte', 
            sender='mailtrap@superbowlstania.com', 
            recipients=[email]
        )
        msg.body = f'Bonjour {prenom}, cliquez sur le lien pour valider votre compte: {confirmation_url}'

        mail.send(msg)
    return redirect(url_for('connexion.reussite_creation_compte'))

@connexion_bp.route('/confirmer/<token>')
def confirmer_compte(token):
    mysql = current_app.extensions['mysql']
    conn = mysql.connect()
    cursor = conn.cursor()
    update_query = 'UPDATE users SET confirmed = 1 WHERE token = %s'
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
    mysql = current_app.extensions['mysql']
    email = request.form.get('inputEmail')
    mot_de_passe = request.form.get('inputPass')
    conn = mysql.connect()
    curseur = conn.cursor()
    requete_select = "SELECT * FROM users WHERE email = %s"
    curseur.execute(requete_select, (email,))
    utilisateur = curseur.fetchone()
    curseur.close()
    conn.close()
    if utilisateur:
        mot_de_passe_hashe = utilisateur[4]
        if check_password_hash(mot_de_passe_hashe, mot_de_passe):
            if utilisateur[6] == 1:
                session['id_utilisateur'] = utilisateur[0]
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
    mysql = current_app.extensions['mysql']
    if 'id_utilisateur' in session:
        id_utilisateur = session['id_utilisateur']
        conn = mysql.connect()
        curseur = conn.cursor()
        curseur.execute("SELECT role FROM users WHERE id = %s", (id_utilisateur,))
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
    mysql = current_app.extensions['mysql']
    mail = current_app.extensions['mail']
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['inputEmail']
        nouveau_mot_de_passe = generer_mot_de_passe(8)
        mot_de_passe_hashe = generate_password_hash(nouveau_mot_de_passe)
        conn = mysql.connect()
        cursor = conn.cursor()
        update_query = 'UPDATE users SET mot_de_passe = %s WHERE email = %s'
        cursor.execute(update_query, (mot_de_passe_hashe, email))
        conn.commit()
        cursor.close()
        conn.close()
        msg = Message(
            "Récupération de mot de passe",
            sender='mailtrap@superbowlstania.com',
            recipients=[email]
        )
        msg.body = f"Bonjour {nom},\n\nVotre nouveau mot de passe est : {nouveau_mot_de_passe}\n\nMerci."
        mail.send(msg)
        return render_template('mot_de_passe_confirmation.html', message_mot="L'email a été envoyé avec succès.")

    return render_template('mot_de_passe_oublie.html')

@connexion_bp.route('/mot_de_passe_oublie', methods=['GET'])
def mot_de_passe_oublie():
    return render_template("mot_de_passe_oublie.html")


@connexion_bp.route('/changer_mot_de_passe', methods=['GET', 'POST'])
def changer_mot_de_passe():
    mysql = current_app.extensions['mysql']    
    if 'id_utilisateur' not in session:
        return redirect(url_for('connexion.se_connecter'))
    if request.method == 'POST':
        mot_de_passe_actuel = request.form.get('inputMdp')
        nouveau_mot_de_passe = request.form.get('inputModificationMdp')
        id_utilisateur = session['id_utilisateur']
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT mot_de_passe FROM users WHERE id = %s"
        cursor.execute(query, (id_utilisateur,))
        result = cursor.fetchone()
        if result is None:
            cursor.close()
            conn.close()
            flash("Utilisateur introuvable.", "danger")
            return redirect(url_for('connexion.se_connecter'))
        mot_de_passe_hash = result[0]
        if not check_password_hash(mot_de_passe_hash, mot_de_passe_actuel):
            cursor.close()
            conn.close()
            flash("Le mot de passe actuel est incorrect.", "danger")
            return redirect(url_for('connexion.changer_mot_de_passe'))
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
    @wraps(func)
    def decorated_function(*args, **kwargs):
        mysql = current_app.extensions['mysql']
        if 'id_utilisateur' in session:
            id_utilisateur = session['id_utilisateur']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE id = %s", (id_utilisateur,))
            result = cursor.fetchone()
            if result is not None:
                role = result[0]
                if role == 'admin':
                    cursor.close()
                    conn.close()
                    return func(*args, **kwargs)
            cursor.close()
            conn.close()
        return redirect(url_for('index'))
    return decorated_function

@connexion_bp.route('/deconnecter_utilisateur', methods=['POST'])
def deconnecter_utilisateur():
    session.pop('id_utilisateur', None)
    return '', 204

@connexion_bp.route('/deconnexion_user_bouton', methods=['POST'])
def deconnexion_user_bouton():
    session.pop('id_utilisateur', None)
    return redirect(url_for('index'))
