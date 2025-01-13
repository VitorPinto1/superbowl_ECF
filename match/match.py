from api.config import Blueprint, fake, Faker, random
from api.app import *
match_bp = Blueprint('match', __name__, template_folder='templates')


class Matchs:
    def __init__(self, equipe1, equipe2, jour, debut, fin, statut, score, meteo, cote1, cote2, commentaires, joueurs_equipe1, joueurs_equipe2, logo_equipe1, logo_equipe2, vainqueur ):
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
        self.logo_equipe1 = logo_equipe1
        self.logo_equipe2 = logo_equipe2
        self.vainqueur = vainqueur
        
def obtenir_matchs_from_database():
    from api.app import mysql
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
        GROUP_CONCAT(DISTINCT CONCAT(j2.nom_joueur, ' ', j2.prenom_joueur, ' (#', j2.numero_tshirt, ')') ORDER BY j2.nom_joueur SEPARATOR ', ') AS joueurs_equipe2,
        e1.logo AS logo_equipe1,
        e2.logo AS logo_equipe2,
        m.vainqueur
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
        m.equipe1, m.equipe2, m.jour, m.debut, m.fin, m.statut, m.score, m.meteo, m.cote1, m.cote2, m.commentaires, e1.logo, e2.logo, m.vainqueur
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
        if match.vainqueur is None:
            match.vainqueur = ' - '

        matchs.append(match)

    cursor.close()
    conn.close()
    return matchs
    
    


def generer_meteo_aleatoire():
    conditions = ["Ensoleillé", "Nuageux", "Pluvieux", "Venteux", "Neigeux"]
    temperature = random.randint(-10, 35)  # Température aléatoire entre -10 et 35 degrés
    condition = random.choice(conditions)
    meteo = f"{condition}, {temperature}°C"
    return meteo



def random_prenom(equipe_id, numero_joueurs = 11):
    joueurs_prenom = []
    for _ in range(numero_joueurs):
        nom_complet = fake.name()
        nom_parts = nom_complet.split(' ')
        nom_joueur = nom_parts[0]
        if len(nom_parts) > 1:
            prenom_joueur = ' '.join(nom_parts[1:])  
        else:
            prenom_joueur = ''
        numero_tshirt = random.randint(1,99)
        joueurs_prenom.append((nom_joueur, prenom_joueur, numero_tshirt, equipe_id))
    return joueurs_prenom

def ajouter_joueurs(joueurs_prenom):
    from api.app import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    for joueur_prenom in joueurs_prenom:
        insert_query = "INSERT INTO joueurs (nom_joueur, prenom_joueur, numero_tshirt, equipe_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, joueur_prenom)

    conn.commit()
    cursor.close()
    conn.close()

def verifier_existence_joueurs(equipe_id):
    from api.app import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM joueurs WHERE equipe_id = %s", (equipe_id,))
    (count,) = cursor.fetchone()
    cursor.close()
    conn.close()
    return count > 0

equipes_ids = list(range(1, 33))  

for equipe_id in equipes_ids:
    if not verifier_existence_joueurs(equipe_id):
        joueurs_prenom = random_prenom(equipe_id)
        ajouter_joueurs(joueurs_prenom)

def generer_matchs_quotidiens():
    """Génère automatiquement des matchs chaque jour, en vérifiant s'il y a déjà des matchs."""
    from api.app import mysql
    from datetime import datetime, timedelta
    import random


    conn = mysql.connect()
    cursor = conn.cursor()

    # Récupérer la date cible (par défaut demain)
    jour = (datetime.now() + timedelta(days=1)).date()

    # Vérifier s'il existe déjà des matchs pour cette date
    cursor.execute("SELECT COUNT(*) FROM matchs WHERE jour = %s", (jour,))
    nb_matchs = cursor.fetchone()[0]

    if nb_matchs > 0:
        conn.close()
        print(f"Des matchs ont déjà été générés pour le {jour}. Aucun nouveau match ne sera créé.")
        return

    # Récupérer les équipes disponibles
    cursor.execute("SELECT nom_equipe FROM equipes")
    equipes = [equipe[0] for equipe in cursor.fetchall()]

    if len(equipes) < 2:
        conn.close()
        print("Erreur : Pas assez d'équipes pour générer des matchs.")
        return

    # Mélanger les équipes et former des matchs
    random.shuffle(equipes)
    matchs = []

    for i in range(0, len(equipes) - 1, 2):
        equipe1 = equipes[i]
        equipe2 = equipes[i + 1]
        debut = f"{random.randint(14, 20)}:00"  # Heure aléatoire entre 14:00 et 20:00
        cote1 = round(random.uniform(1.5, 3.5), 2)
        cote2 = round(random.uniform(1.5, 3.5), 2)
        statut = "À venir"
        meteo = generer_meteo_aleatoire()

        matchs.append((equipe1, equipe2, jour, debut, cote1, cote2, statut, meteo))

        if len(matchs) == 4:  # Limiter à 4 matchs
            break

    # Insérer les matchs dans la base de données
    for match in matchs:
        cursor.execute("""
            INSERT INTO matchs (equipe1, equipe2, jour, debut, cote1, cote2, statut, meteo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, match)

    conn.commit()
    conn.close()
    print(f"4 matchs pour le {jour} ont été générés avec succès.")
