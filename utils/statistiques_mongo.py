from flask import current_app
import os

def sync_mises_to_mongo():
    mongo = current_app.extensions['mongo']
    mysql = current_app.extensions['mysql']
    
    # Conexión a MySQL y obtención del cursor
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # Referencias a las colecciones en MongoDB
    mises_collection = mongo.db.mises
    matchs_collection = mongo.db.matchs  # Se generará a partir de los datos sincronizados

    # Reiniciamos ambas colecciones para evitar duplicados
    mises_collection.delete_many({})
    matchs_collection.delete_many({})

    query = """
    SELECT 
        m.id AS id_mise,
        m.mise1, m.mise2, m.resultat1, m.resultat2,
        ma.equipe1 AS match_equipe1, 
        ma.equipe2 AS match_equipe2,
        m.cote1, m.cote2, m.datemise,
        u.id AS id_utilisateur, u.nom, u.prenom,
        ma.id AS id_match, ma.jour, ma.debut, ma.fin, ma.score, ma.vainqueur
    FROM mises m
    JOIN users u ON m.id_utilisateur = u.id
    JOIN matchs ma ON m.id_match = ma.id
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Recuperamos los nombres de las columnas
    columns = [desc[0] for desc in cursor.description]
    
    bet_docs = []
    match_docs = {}
    
    for row in rows:
        row_dict = dict(zip(columns, row))
        
        # Conversión de valores numéricos y cálculo de ganancias
        try:
            mise1 = float(row_dict["mise1"]) if row_dict["mise1"] is not None else 0.0
            mise2 = float(row_dict["mise2"]) if row_dict["mise2"] is not None else 0.0
            resultat1 = float(row_dict["resultat1"]) if row_dict["resultat1"] is not None else 0.0
            resultat2 = float(row_dict["resultat2"]) if row_dict["resultat2"] is not None else 0.0
        except Exception as e:
            mise1 = mise2 = resultat1 = resultat2 = 0.0

        gain1 = resultat1 - mise1
        gain2 = resultat2 - mise2

        # Documento de apuesta (bet) con información del usuario, partido y apuestas
        bet_doc = {
            "id_mise": row_dict["id_mise"],
            "utilisateur": {
                "id": row_dict["id_utilisateur"],
                "nom": row_dict["nom"],
                "prenom": row_dict["prenom"]
            },
            "match": {
                "id": row_dict["id_match"],
                "equipe1": row_dict["match_equipe1"],
                "equipe2": row_dict["match_equipe2"],
                "jour": str(row_dict["jour"]),
                "debut": row_dict["debut"],
                "fin": row_dict["fin"],
                "score": row_dict["score"],
                "vainqueur": row_dict["vainqueur"]
            },
            "bets": [
                {
                    "team": row_dict["match_equipe1"],
                    "mise": mise1,
                    "cote": row_dict["cote1"],
                    "resultat": resultat1,
                    "gain": gain1
                },
                {
                    "team": row_dict["match_equipe2"],
                    "mise": mise2,
                    "cote": row_dict["cote2"],
                    "resultat": resultat2,
                    "gain": gain2
                }
            ],
            "datemise": str(row_dict["datemise"])
        }
        bet_docs.append(bet_doc)
        
        # Construimos un documento único por partido, usando el id del partido como clave
        match_id = row_dict["id_match"]
        if match_id not in match_docs:
            match_docs[match_id] = {
                "id": match_id,
                "equipe1": row_dict["match_equipe1"],
                "equipe2": row_dict["match_equipe2"],
                "jour": str(row_dict["jour"]),
                "debut": row_dict["debut"],
                "fin": row_dict["fin"],
                "score": row_dict["score"],
                "vainqueur": row_dict["vainqueur"]
            }
    
    # Inserción en bloque para mayor rendimiento
    if bet_docs:
        mises_collection.insert_many(bet_docs)
    
    if match_docs:
        matchs_collection.insert_many(list(match_docs.values()))
    
    cursor.close()
    conn.close()
