from flask import current_app
import os

def sync_mises_to_mongo():
    mongo = current_app.extensions['mongo']
    mysql = current_app.extensions['mysql']
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # Collection pour les stats par match
    match_stats_collection = mongo.db.match_stats  
    match_stats_collection.delete_many({})

    query_match_stats = """
    SELECT 
        ma.id AS id_match,
        ma.equipe1,
        ma.equipe2,
        COUNT(CASE WHEN m.mise1 > 0 THEN 1 END) AS nb_paris_equipe1,
        COUNT(CASE WHEN m.mise2 > 0 THEN 1 END) AS nb_paris_equipe2,
        CONCAT(
            ROUND(COUNT(CASE WHEN m.mise1 > 0 THEN 1 END) * 100.0 /
            (COUNT(CASE WHEN m.mise1 > 0 THEN 1 END) + COUNT(CASE WHEN m.mise2 > 0 THEN 1 END)), 2), '%'
        ) AS pourcentage_equipe1,
        CONCAT(
            ROUND(COUNT(CASE WHEN m.mise2 > 0 THEN 1 END) * 100.0 /
            (COUNT(CASE WHEN m.mise1 > 0 THEN 1 END) + COUNT(CASE WHEN m.mise2 > 0 THEN 1 END)), 2), '%'
        ) AS pourcentage_equipe2
    FROM mises m
    JOIN matchs ma ON m.id_match = ma.id
    GROUP BY ma.id, ma.equipe1, ma.equipe2
    ORDER BY ma.id;
    """

    cursor.execute(query_match_stats)
    rows_match_stats = cursor.fetchall()
    
    columns_match_stats = [desc[0] for desc in cursor.description]
    
    match_stats_docs = []
    
    for row in rows_match_stats:
        row_dict = dict(zip(columns_match_stats, row))
        doc = {
            "id_match": row_dict["id_match"],
            "equipe1": row_dict["equipe1"],
            "equipe2": row_dict["equipe2"],
            "nb_paris_equipe1": row_dict["nb_paris_equipe1"],
            "nb_paris_equipe2": row_dict["nb_paris_equipe2"],
            "pourcentage_equipe1": row_dict["pourcentage_equipe1"],
            "pourcentage_equipe2": row_dict["pourcentage_equipe2"]
        }
        match_stats_docs.append(doc)
    
    if match_stats_docs:
        match_stats_collection.insert_many(match_stats_docs)
    
    
    # Collection pour les stats par utilisateur
    user_stats_collection = mongo.db.user_stats  
    user_stats_collection.delete_many({})

    query_user_stats = """
    SELECT 
    t.id_utilisateur,
    t.nom,
    t.prenom,
    t.total_gagnes,
    t.total_pertes,
    CASE 
        WHEN (t.total_gagnes + t.total_pertes) = 0 THEN 0
        ELSE ROUND((t.total_gagnes / (t.total_gagnes + t.total_pertes)) * 100, 2)
    END AS pourcentage_gagnes,
    CASE 
        WHEN (t.total_gagnes + t.total_pertes) = 0 THEN 0
        ELSE ROUND((t.total_pertes / (t.total_gagnes + t.total_pertes)) * 100, 2)
    END AS pourcentage_pertes
    FROM (
    SELECT
        u.id AS id_utilisateur,
        u.nom,
        u.prenom,
        -- Calcul du total des gains sur les paris gagnants :
        SUM(
        CASE
            WHEN (ma.vainqueur = ma.equipe1 AND m.mise1 > 0)
                OR (ma.vainqueur = ma.equipe2 AND m.mise2 > 0)
            THEN CASE 
                WHEN ma.vainqueur = ma.equipe1 THEN (m.resultat1 - m.mise1)
                ELSE (m.resultat2 - m.mise2)
                END
            ELSE 0
        END
        ) AS total_gagnes,
        -- Calcul du total des pertes (en valeur positive) sur les paris perdants :
        ABS(SUM(
        CASE
            WHEN (ma.vainqueur = ma.equipe1 AND m.mise2 > 0)
                OR (ma.vainqueur = ma.equipe2 AND m.mise1 > 0)
            THEN CASE
                WHEN ma.vainqueur = ma.equipe1 THEN -m.mise2
                ELSE -m.mise1
                END
            ELSE 0
        END
        )) AS total_pertes
    FROM mises m
    JOIN users u ON m.id_utilisateur = u.id
    JOIN matchs ma ON m.id_match = ma.id
    GROUP BY u.id, u.nom, u.prenom
    ) t;

    """

    cursor.execute(query_user_stats)
    rows_user_stats = cursor.fetchall()
    
    columns_user_stats = [desc[0] for desc in cursor.description]
    
    user_stats_docs = []
    
    for row in rows_user_stats:
        row_dict = dict(zip(columns_user_stats, row))
        doc = {
            "id_utilisateur": row_dict["id_utilisateur"],
            "nom": row_dict["nom"],
            "prenom": row_dict["prenom"],
            "total_gagnes": float(row_dict["total_gagnes"]),
            "total_pertes": float(row_dict["total_pertes"]),    
            "pourcentage_gagnes": float(row_dict["pourcentage_gagnes"]),
            "pourcentage_pertes": float(row_dict["pourcentage_pertes"])
        }
        user_stats_docs.append(doc)
    
    if user_stats_docs:
        user_stats_collection.insert_many(user_stats_docs)
    
    cursor.close()
    conn.close()
