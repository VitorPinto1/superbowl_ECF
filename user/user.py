from api.config import *


user_bp = Blueprint('user', __name__, template_folder='templates')


@user_bp.route('/espace_utilisateur', methods=['GET'])
def espace_utilisateur():
    from api.app import mysql
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
        SELECT 
            mises.id, matchs.equipe1, matchs.equipe2, matchs.jour, matchs.debut, matchs.fin, mises.mise1, mises.mise2, mises.resultat1, mises.resultat2, matchs.statut, matchs.vainqueur, mises.equipe1, mises.equipe2, mises.datemise,
            e1.logo AS logo_equipe1, e2.logo AS logo_equipe2
        FROM mises
        JOIN matchs ON mises.id_match = matchs.id
        LEFT JOIN 
            equipes e1 ON matchs.equipe1 = e1.nom_equipe
        LEFT JOIN 
            equipes e2 ON matchs.equipe2 = e2.nom_equipe
        WHERE mises.id_utilisateur = %s 
        ORDER BY 
            CASE matchs.statut 
                WHEN 'En cours' THEN 1
                WHEN 'Terminé' THEN 2
                WHEN 'À venir' THEN 3
                ELSE 4
            END,
            matchs.jour

    '''
    cursor.execute(select_mises_query, (id_utilisateur,))
    mises = cursor.fetchall()
    cursor.close()
    conn.close()
    # Renvoyer le modèle avec les informations utilisateur
    return render_template('espace_utilisateur.html', utilisateur = utilisateur, mises=mises)
