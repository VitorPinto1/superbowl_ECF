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
  matchs = list(mongo.db.matchs_year.find().sort("year", 1))


  return render_template('records_admin.html', matchs=matchs)




# longueurs maximales pour chaque champ
LONGUEURS_CHAMPS = {
    'super_bowl': 5,
    'winner': 50,
    'loser': 50,
    'result': 20,
    'location.stadium': 50,
    'location.city': 50,
    'location.state': 50,
    'weather': 50,
    'mvp': 50,
    'attendance': 10,
}

def valider_longueur_champs(donnees):
    for champ, longueur_max in LONGUEURS_CHAMPS.items():
        cles = champ.split('.')
        valeur = donnees
        for cle in cles:
            valeur = valeur.get(cle, {})
        
        # Validation pour les chaînes de caractères
        if isinstance(valeur, str) and len(valeur) > longueur_max:
            return f"Le champ '{champ}' dépasse la longueur maximale autorisée de {longueur_max} caractères."
        
        # Validation pour les entiers (convertibles)
        if champ in ['year', 'attendance', 'super_bowl']:
            if not isinstance(valeur, int):
                try:
                    valeur = int(valeur)  # Tente de convertir en entier
                except ValueError:
                    return f"Le champ '{champ}' doit être un entier valide."
            if len(str(valeur)) > longueur_max:
                return f"Le champ '{champ}' dépasse la longueur maximale autorisée de {longueur_max} chiffres."
    
    return None


@admin_bp.route('/update_match', methods=['POST'])
@admin_required
def update_match():
    data = request.json
    match_id = data.get('_id')  
    updates = data.get('updates')  

    if not match_id or not updates:
        return jsonify({'error': 'ID ou donnes manquants'}), 400
    
     # Validation de la longueur
    validation_error = valider_longueur_champs(updates)
    if validation_error:
        return jsonify({'error': validation_error}), 400

    try:
        # Validation de l'ID MongoDB
        try:
            match_id = ObjectId(match_id)
        except InvalidId:
            return jsonify({'error': 'Invalid ID format'}), 400

        # Mise à jour des données dans la base MongoDB
        mongo.db.matchs_year.update_one({'_id': match_id}, {'$set': updates})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': 'Une erreur est survenue'}), 500
    
@admin_bp.route('/add_match', methods=['POST'])
@admin_required
def add_match():
    data = request.json

    REQUIRED_FIELDS = {
        'year': 4,  
        'super_bowl': 5,  
        'winner': 50,
        'loser': 50,
        'result': 20,
        'location.stadium': 100,
        'location.city': 50,
        'location.state': 50,
        'weather': 50,
        'mvp': 50,
        'attendance': 10,  
    }

    def get_nested_value(data, keys):
        """Helper function to get nested value from a dictionary."""
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, None)
            else:
                return None
        return data

    for field, max_length in REQUIRED_FIELDS.items():
        keys = field.split('.')
        value = get_nested_value(data, keys)
        
        # Validation : le champ est obligatoire
        if value is None:
            return jsonify({'error': f"Le champ '{field}' est requis."}), 400

        # Validation de la longueur pour les chaînes
        if isinstance(value, str) and len(value) > max_length:
            return jsonify({'error': f"Le champ '{field}' dépasse la longueur maximale de {max_length} caractères."}), 400

        # Validation et conversion des entiers
        if field in ['year', 'attendance', 'super_bowl']:
            try:
                int_value = int(value)  # Convertir en entier
                if len(str(int_value)) > max_length:  # Vérifier la longueur
                    return jsonify({'error': f"Le champ '{field}' dépasse la longueur maximale de {max_length} chiffres."}), 400
                # Mise à jour de la donnée avec la valeur entière
                if len(keys) == 1:
                    data[keys[0]] = int_value
                else:
                    nested_data = data
                    for key in keys[:-1]:
                        nested_data = nested_data[key]
                    nested_data[keys[-1]] = int_value
            except (ValueError, TypeError):
                return jsonify({'error': f"Le champ '{field}' doit être un entier valide."}), 400
            
    existing_year_match = mongo.db.matchs_year.find_one({'year': data['year']})
    if existing_year_match:
        return jsonify({'error': f"Un match pour l'année '{data['year']}' existe déjà. Vous ne pouvez pas ajouter un autre match pour cette année."}), 400

    existing_super_bowl_match = mongo.db.matchs_year.find_one({'super_bowl': data['super_bowl']})
    if existing_super_bowl_match:
        return jsonify({'error': f"Un match avec le Super Bowl '{data['super_bowl']}' existe déjà."}), 400


    try:
        # Ajouter le match dans MongoDB
        match_id = mongo.db.matchs_year.insert_one(data).inserted_id
        return jsonify({'success': True, 'match_id': str(match_id)}), 201
    except Exception as e:
        return jsonify({'error': f"Une erreur est survenue lors de l’ajout du match : {str(e)}"}), 500



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
