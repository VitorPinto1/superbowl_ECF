from api.config import *
from api.app import *
from connexion.connexion import *
from match.match import generer_meteo_aleatoire


admin_bp = Blueprint('admin', __name__, template_folder='templates')



@admin_bp.route('/espace_administrateur')
@admin_required
def espace_administrateur():
    return render_template('espace_administrateur.html')


@admin_bp.route('/creation')
@admin_required
def creation():
    return render_template('creation.html')

@admin_bp.route('/creation', methods=['POST'])
@admin_required
def creation_form():
    from api.app import mysql
    nom_equipe = request.form.get('nom_equipe')
    pays_appartenance = request.form.get('pays_appartenance')

    conn = mysql.connect()
    cursor = conn.cursor()

    # Vérifier si l'équipe existe déjà dans la base de données
    check_query = "SELECT * FROM equipes WHERE nom_equipe = %s"
    cursor.execute(check_query, (nom_equipe,))
    equipe_deja_utilise = cursor.fetchone()

    if equipe_deja_utilise:
        erreur = "Équipe déjà créée"
        return render_template('creation.html', erreur=erreur)
    else:
        insert_equipe_query = "INSERT INTO equipes (nom_equipe, pays_appartenance) VALUES (%s, %s)"
        equipe_data = (nom_equipe, pays_appartenance)
        cursor.execute(insert_equipe_query, equipe_data)
        equipe_id = cursor.lastrowid # renvoie la valeur de l'ID de la dernière ligne

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

    return redirect(url_for('admin.espace_administrateur'))

@admin_bp.route('/planification', methods=['GET', 'POST'])

@admin_required

def planification_form():
    from api.app import mysql
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
        return redirect(url_for('index'))
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT nom_equipe FROM equipes")
    equipes = [equipe[0] for equipe in cursor.fetchall()]
    conn.close()
    return render_template('planification.html', equipes = equipes)

@admin_bp.route('/planification')
@admin_required
def planification():
    return render_template('planification.html')

@admin_bp.route('/records_admin')
@admin_required
def records_admin():
  matchs = list(mongo.db.matchs_year.find())


  return render_template('records_admin.html', matchs=matchs)





@admin_bp.route('/update_match', methods=['POST'])
@admin_required
def update_match():
    data = request.json
    match_id = data.get('_id')  
    updates = data.get('updates')  

    if not match_id or not updates:
        return jsonify({'error': 'ID ou donnes manquants'}), 400

    try:
        mongo.db.matchs_year.update_one({'_id': ObjectId(match_id)}, {'$set': updates})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/delete_match', methods=['POST'])
@admin_required
def delete_match():
    data = request.json
    match_id = data.get('_id')  

    if not match_id:
        return jsonify({'error': 'ID manquant'}), 400

    try:
        mongo.db.matchs_year.delete_one({'_id': ObjectId(match_id)})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
