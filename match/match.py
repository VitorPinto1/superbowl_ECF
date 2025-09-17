from api.config import *
from flask import current_app

match_bp = Blueprint('match', __name__, template_folder='templates')

fake = Faker()

class Matchs:
    def __init__(
        self, equipe1, equipe2, jour, debut, fin, statut, score, meteo,
        cote1, cote2, commentaires, joueurs_equipe1, joueurs_equipe2,
        logo_equipe1, logo_equipe2, vainqueur
    ):
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.jour = jour
        self.debut = debut
        self.fin = fin if fin is not None else ' - '
        self.statut = statut if statut is not None else ' - '
        self.score = score if score is not None else ' - '
        self.meteo = meteo if meteo is not None else ' - '
        self.cote1 = cote1
        self.cote2 = cote2
        self.commentaires = commentaires if commentaires is not None else ' - '
        self.joueurs_equipe1 = joueurs_equipe1
        self.joueurs_equipe2 = joueurs_equipe2
        self.logo_equipe1 = logo_equipe1 if logo_equipe1 is not None else 'sources/default_logo.png'
        self.logo_equipe2 = logo_equipe2 if logo_equipe2 is not None else 'sources/default_logo.png'

        self.vainqueur = vainqueur if vainqueur is not None else ' - '

def obtenir_matchs_from_database():
    mysql = current_app.extensions['mysql']
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
            GROUP_CONCAT(
                DISTINCT CONCAT(j1.nom_joueur, ' ', j1.prenom_joueur, ' (#', j1.numero_tshirt, ')')
                ORDER BY j1.nom_joueur SEPARATOR ', '
            ) AS joueurs_equipe1,
            GROUP_CONCAT(
                DISTINCT CONCAT(j2.nom_joueur, ' ', j2.prenom_joueur, ' (#', j2.numero_tshirt, ')')
                ORDER BY j2.nom_joueur SEPARATOR ', '
            ) AS joueurs_equipe2,
            e1.logo AS logo_equipe1,
            e2.logo AS logo_equipe2,
            m.vainqueur
        FROM matchs m
        LEFT JOIN equipes e1 ON m.equipe1 = e1.nom_equipe
        LEFT JOIN joueurs j1 ON e1.id = j1.equipe_id
        LEFT JOIN equipes e2 ON m.equipe2 = e2.nom_equipe
        LEFT JOIN joueurs j2 ON e2.id = j2.equipe_id
        GROUP BY 
            m.equipe1, m.equipe2, m.jour, m.debut, m.fin, m.statut, m.score,
            m.meteo, m.cote1, m.cote2, m.commentaires, e1.logo, e2.logo, m.vainqueur
        ORDER BY 
            CASE m.statut 
                WHEN 'En cours' THEN 1
                WHEN 'À venir' THEN 2
                WHEN 'Terminé' THEN 3
                ELSE 4
            END,
            m.jour
    '''
    cursor.execute(select_query)
    matchs_data = cursor.fetchall()
    matchs = []
    for match_data in matchs_data:
        match = Matchs(*match_data)
        matchs.append(match)
    cursor.close()
    conn.close()
    return matchs

def generer_meteo_aleatoire():
    conditions = ["Ensoleillé", "Nuageux", "Pluvieux", "Venteux", "Neigeux"]
    temperature = random.randint(-10, 35)
    condition = random.choice(conditions)
    return f"{condition}, {temperature}°C"

def random_prenom(equipe_id, numero_joueurs=11):
    joueurs_prenom = []
    for _ in range(numero_joueurs):
        nom_complet = fake.name()
        nom_parts = nom_complet.split(' ')
        nom_joueur = nom_parts[0]
        prenom_joueur = ' '.join(nom_parts[1:]) if len(nom_parts) > 1 else ''
        numero_tshirt = random.randint(1, 99)
        joueurs_prenom.append((nom_joueur, prenom_joueur, numero_tshirt, equipe_id))
    return joueurs_prenom

def ajouter_joueurs(joueurs_prenom):
    mysql = current_app.extensions['mysql']
    conn = mysql.connect()
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO joueurs (nom_joueur, prenom_joueur, numero_tshirt, equipe_id)
        VALUES (%s, %s, %s, %s)
    """
    cursor.executemany(insert_query, joueurs_prenom)
    conn.commit()
    cursor.close()
    conn.close()

def verifier_existence_joueurs(equipe_id):
    mysql = current_app.extensions['mysql']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM joueurs WHERE equipe_id = %s", (equipe_id,))
    (count,) = cursor.fetchone()
    cursor.close()
    conn.close()
    return count > 0

def initialiser_joueurs():
    for equipe_id in range(1, 33):
        if not verifier_existence_joueurs(equipe_id):
            joueurs_prenom = random_prenom(equipe_id)
            ajouter_joueurs(joueurs_prenom)

def generer_matchs_quotidiens():
    mysql = current_app.extensions['mysql']
    conn = mysql.connect()
    cursor = conn.cursor()
    jour = (datetime.now() + timedelta(days=1)).date()
    cursor.execute("SELECT COUNT(*) FROM matchs WHERE jour = %s", (jour,))
    nb_matchs = cursor.fetchone()[0]
    if nb_matchs > 0:
        conn.close()
        print(f"Des matchs ont déjà été générés pour le {jour}. Aucun nouveau match ne sera créé.")
        return
    cursor.execute("SELECT nom_equipe FROM equipes")
    equipes = [equipe[0] for equipe in cursor.fetchall()]
    if len(equipes) < 2:
        conn.close()
        print("Erreur : Pas assez d'équipes pour générer des matchs.")
        return
    random.shuffle(equipes)
    matchs = []
    for i in range(0, len(equipes) - 1, 2):
        equipe1 = equipes[i]
        equipe2 = equipes[i + 1]
        debut = f"{random.randint(14, 20)}:00"
        cote1 = round(random.uniform(1.5, 3.5), 2)
        cote2 = round(random.uniform(1.5, 3.5), 2)
        statut = "À venir"
        meteo = generer_meteo_aleatoire()
        matchs.append((equipe1, equipe2, jour, debut, cote1, cote2, statut, meteo))
        if len(matchs) == 4:
            break
    for match in matchs:
        cursor.execute("""
            INSERT INTO matchs (equipe1, equipe2, jour, debut, cote1, cote2, statut, meteo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, match)
    conn.commit()
    conn.close()
    print(f"4 matchs pour le {jour} ont été générés avec succès.")


def mettre_a_jour_tous_les_statuts():
    """Met à jour tous les statuts des matchs (À venir -> En cours -> Terminé)"""
    mysql = current_app.extensions['mysql']
    conn = mysql.connect()
    cursor = conn.cursor()
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    
    # 1. Mettre à jour À venir -> En cours
    cursor.execute("""
        UPDATE matchs
        SET statut = 'En cours'
        WHERE jour = %s AND debut <= %s AND statut = 'À venir'
    """, (current_date, current_time))
    updated_en_cours = cursor.rowcount
    
    # 2. Mettre à jour En cours -> Terminé
    # Sélectionner seulement les matchs qui sont vraiment terminés
    # On exclut les matchs qui viennent d'être mis "En cours" (statut = 'En cours')
    cursor.execute("""
        SELECT id, equipe1, equipe2, but1, but2, statut, vainqueur, jour, fin
        FROM matchs
        WHERE (
            statut = 'En cours'
            AND jour < %s
        )
        OR (
            statut = 'En cours'
            AND jour = %s 
            AND fin IS NOT NULL 
            AND fin <= %s
        )
        OR (
            statut = 'Terminé'
            AND (vainqueur IS NULL OR LENGTH(vainqueur) < 5)
        )
    """, (current_date, current_date, current_time))
    
    matchs_a_terminer = cursor.fetchall()
    updated_terminé = 0
    
    for match in matchs_a_terminer:
        id_match, equipe1, equipe2, but1, but2, statut, vainqueur, jour, fin = match
        
            
        # Générer les scores si nécessaire
        if but1 is None or but2 is None:
            but1 = random.randint(0, 50) if but1 is None else but1
            but2 = random.randint(0, 50) if but2 is None else but2
        
        # Déterminer le vainqueur
        if not vainqueur or len(vainqueur.strip()) < 5:
            if but1 > but2:
                vainqueur = equipe1
            elif but2 > but1:
                vainqueur = equipe2
            else:
                vainqueur = "Égalité"
        
        # Mettre à jour le match
        cursor.execute("""
            UPDATE matchs
            SET but1 = %s, but2 = %s, statut = 'Terminé', vainqueur = %s
            WHERE id = %s
        """, (but1, but2, vainqueur, id_match))
        updated_terminé += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    if updated_en_cours > 0 or updated_terminé > 0:
        print(f"Scheduler: {updated_en_cours} match(s) mis à 'En cours', {updated_terminé} match(s) terminés.")
