
from flask import current_app

from api.config import *
from match.match import obtenir_matchs_from_database


paris_bp = Blueprint('paris', __name__, template_folder='templates')

@paris_bp.route('/visualiser_matchs')
def visualiser_matchs():
    mysql = current_app.extensions['mysql']
    matchs = obtenir_matchs_from_database()
    voir_bouton_miser = False

    if 'id_utilisateur' in session:
        id_utilisateur = session['id_utilisateur']
        conn = mysql.connect()
        curseur = conn.cursor()
        curseur.execute("SELECT role FROM users WHERE id = %s", (id_utilisateur,))
        role = curseur.fetchone()[0]
        curseur.close()
        conn.close()
        if role == 'user':
            voir_bouton_miser = True

    return render_template('visualiser_matchs.html', voir_bouton_miser=voir_bouton_miser, matchs=matchs)

@paris_bp.route('/store_in_session', methods=['POST'])
def store_in_session():
    session['equipe1'] = request.form.get('equipe1')
    session['equipe2'] = request.form.get('equipe2')
    session['cote1'] = request.form.get('cote1')
    session['cote2'] = request.form.get('cote2')
    session['mise1'] = request.form.get('mise1')
    session['mise2'] = request.form.get('mise2')
    session['jour'] = request.form.get('jour')
    session['debut'] = request.form.get('debut')
    return redirect(url_for('paris.miser'))

@paris_bp.route('/miser')
def miser():
    mysql = current_app.extensions['mysql']
    equipe1 = session.get('equipe1')
    equipe2 = session.get('equipe2')
    cote1 = session.get('cote1')
    cote2 = session.get('cote2')
    jour = session.get('jour')
    debut = session.get('debut')
    utilisateur = session['id_utilisateur']

    conn = mysql.connect()
    cursor = conn.cursor()
    select_existing_bet_query = '''
        SELECT id FROM mises
        WHERE id_utilisateur = %s AND id_match IN (
            SELECT id FROM matchs 
            WHERE equipe1 = %s AND equipe2 = %s AND jour = %s AND debut = %s
        )
    '''
    cursor.execute(select_existing_bet_query, (utilisateur, equipe1, equipe2, jour, debut))
    existing_bet = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'miser.html',
        equipe1=equipe1,
        equipe2=equipe2,
        cote1=cote1,
        cote2=cote2,
        jour=jour,
        debut=debut,
        existing_bet=existing_bet
    )

@paris_bp.route('/form_miser', methods=['POST'])
def form_miser():
    mysql = current_app.extensions['mysql']
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
    select_match_query = """
        SELECT id FROM matchs 
        WHERE equipe1 = %s AND equipe2 = %s AND jour = %s AND debut = %s
    """
    cursor.execute(select_match_query, (equipe1, equipe2, jour, debut))
    match = cursor.fetchone()
    id_match = match[0]

    select_existing_bet_query = '''
        SELECT id, equipe1, equipe2 
        FROM mises 
        WHERE id_utilisateur = %s AND id_match = %s
    '''
    cursor.execute(select_existing_bet_query, (utilisateur, id_match))
    existing_bets = cursor.fetchall()

    if existing_bets:
        for existing_bet in existing_bets:
            if mise1 is not None and mise1.strip() == "0" and existing_bet[1] == equipe1:
                delete_query1 = "DELETE FROM mises WHERE id = %s"
                cursor.execute(delete_query1, (existing_bet[0],))
              

            elif existing_bet[1] == equipe1 and mise1 is not None and mise1.strip() != "":
                update_query1 = """
                    UPDATE mises
                    SET mise1 = %s, resultat1 = %s
                    WHERE id = %s
                """
                resultat1 = Decimal(mise1) * Decimal(cote1)
                data1 = (Decimal(mise1), resultat1, existing_bet[0])
                cursor.execute(update_query1, data1)

              

            if mise2 is not None and mise2.strip() == "0" and existing_bet[2] == equipe2:
                delete_query2 = "DELETE FROM mises WHERE id = %s"
                cursor.execute(delete_query2, (existing_bet[0],))
              
                
            elif existing_bet[2] == equipe2 and mise2 is not None and mise2.strip() != "":
                update_query2 = """
                    UPDATE mises
                    SET mise2 = %s, resultat2 = %s
                    WHERE id = %s
                """
                resultat2 = Decimal(mise2) * Decimal(cote2)
                data2 = (Decimal(mise2), resultat2, existing_bet[0])
                cursor.execute(update_query2, data2)
                
        conn.commit()
    else:
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
    return redirect(url_for('user.espace_utilisateur'))

@paris_bp.route('/mise/<int:mise_id>/modifier', methods=['GET'])
def modifier_mise(mise_id):
    mysql = current_app.extensions['mysql']
    conn = mysql.connect()
    curseur = conn.cursor()
    requete_select = """
        SELECT mises.*, matchs.equipe1, matchs.equipe2, matchs.cote1, matchs.cote2,
               matchs.jour, matchs.debut
        FROM mises
        INNER JOIN matchs ON mises.id_match = matchs.id
        WHERE mises.id = %s
    """
    curseur.execute(requete_select, (mise_id,))
    mise = curseur.fetchone()

    if mise:
        equipe2 = mise[12]
        equipe1 = mise[13] 
        cote1 = mise[14]
        cote2 = mise[15]
        jour = mise[16]
        debut = mise[17]
        curseur.close()
        conn.close()

        conn = mysql.connect()
        curseur = conn.cursor()
        requete_delete = "DELETE FROM mises WHERE id = %s"
        curseur.execute(requete_delete, (mise_id,))
        conn.commit()

        

       

        curseur.close()
        conn.close()

        return render_template(
            'miser.html',
            equipe1=equipe1,
            equipe2=equipe2,
            cote1=cote1,
            cote2=cote2,
            jour=jour,
            debut=debut
        )
    else:
        curseur.close()
        conn.close()
        return "Mise no disponible"

@paris_bp.route('/mise/<int:mise_id>/supprimer', methods=['GET'])
def supprimer_mise(mise_id):
    mysql = current_app.extensions['mysql']
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
    select_mises_query = '''
        SELECT mises.id, matchs.equipe1, matchs.equipe2, matchs.jour, matchs.debut, 
               matchs.fin, mises.mise1, mises.mise2, mises.resultat1, mises.resultat2, 
               matchs.statut
        FROM mises
        JOIN matchs ON mises.id_match = matchs.id
        WHERE mises.id_utilisateur = %s
    '''
    curseur.execute(select_mises_query, (id_utilisateur,))
    mises = curseur.fetchall()
    curseur.close()
    conn.close()

    return redirect(url_for(
        'user.espace_utilisateur',
        utilisateur=utilisateur,
        mises=mises,
        active_tab='historique',
        suppression='true'
    ))

@paris_bp.route('/parier')
def parier():
    mysql = current_app.extensions['mysql']
    from match.match import obtenir_matchs_from_database
    matchs = obtenir_matchs_from_database()
    voir_bouton_miser_selection = False

    if 'id_utilisateur' in session:
        id_utilisateur = session['id_utilisateur']
        conn = mysql.connect()
        curseur = conn.cursor()
        curseur.execute("SELECT role FROM users WHERE id = %s", (id_utilisateur,))
        role = curseur.fetchone()[0]
        curseur.close()
        conn.close()
        if role == 'user':
            voir_bouton_miser_selection = True

    return render_template(
        'parier.html',
        voir_bouton_miser_selection=voir_bouton_miser_selection,
        matchs=matchs
    )

@paris_bp.route('/miser_sur_la_selection', methods=['POST'])
def miser_sur_la_selection():
    donnees_selectionnees = request.form.get('donnees_selectionnees')
    matchs_selectionnes = json.loads(donnees_selectionnees)
    equipe1 = request.form.get('equipe1')
    equipe2 = request.form.get('equipe2')
    cote1 = request.form.get('cote1')
    cote2 = request.form.get('cote2')
    jour = request.form.get('jour')

    session['miser_sur_la_selection'] = matchs_selectionnes

    return render_template(
        'miser_sur_la_selection.html',
        matchs_selectionnes=matchs_selectionnes,
        equipe1=equipe1,
        equipe2=equipe2,
        cote1=cote1,
        cote2=cote2,
        jour=jour
    )

@paris_bp.route('/form_miser_selection', methods=['POST'])
def form_miser_selection():
    mysql = current_app.extensions['mysql']
    matchs_selectionnes = session.get('miser_sur_la_selection')
    conn = mysql.connect()
    cursor = conn.cursor()

    for index, match_info in enumerate(matchs_selectionnes):
        mise1 = request.form.get(f'mise_equipe1_{index + 1}', '0')
        mise2 = request.form.get(f'mise_equipe2_{index + 1}', '0')

        mise1_decimal = Decimal(mise1) if mise1.isdigit() else Decimal('0')
        mise2_decimal = Decimal(mise2) if mise2.isdigit() else Decimal('0')

        if mise1_decimal == Decimal('0') and mise2_decimal == Decimal('0'):
            continue

        equipe1 = match_info['equipe1']
        equipe2 = match_info['equipe2']
        cote1 = Decimal(match_info['cote1'])
        cote2 = Decimal(match_info['cote2'])
        jour = match_info['jour']
        utilisateur = session['id_utilisateur']
        datemise = datetime.now()

        select_match_query = """
            SELECT id FROM matchs
            WHERE equipe1 = %s AND equipe2 = %s AND jour = %s
        """
        cursor.execute(select_match_query, (equipe1, equipe2, jour))
        match_row = cursor.fetchone()

        if match_row:
            id_match = match_row[0]

            if mise1_decimal > Decimal('0'):
                select_existing_bet_query = """
                    SELECT id FROM mises
                    WHERE id_utilisateur = %s AND id_match = %s AND equipe1 = %s
                """
                cursor.execute(select_existing_bet_query, (utilisateur, id_match, equipe1))
                existing_bet = cursor.fetchone()
                resultat1 = mise1_decimal * cote1

                if existing_bet:
                    update_query = "UPDATE mises SET mise1 = %s, resultat1 = %s WHERE id = %s"
                    cursor.execute(update_query, (mise1_decimal, resultat1, existing_bet[0]))
                else:
                    insert_query = """
                        INSERT INTO mises 
                        (mise1, resultat1, equipe1, cote1, id_utilisateur, id_match, datemise)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        mise1_decimal, resultat1, equipe1, cote1, utilisateur, id_match, datemise
                    ))
                
            

            if mise2_decimal > Decimal('0'):
                select_existing_bet_query = """
                    SELECT id FROM mises
                    WHERE id_utilisateur = %s AND id_match = %s AND equipe2 = %s
                """
                cursor.execute(select_existing_bet_query, (utilisateur, id_match, equipe2))
                existing_bet = cursor.fetchone()
                resultat2 = mise2_decimal * cote2

                if existing_bet:
                    update_query = "UPDATE mises SET mise2 = %s, resultat2 = %s WHERE id = %s"
                    cursor.execute(update_query, (mise2_decimal, resultat2, existing_bet[0]))
                else:
                    insert_query = """
                        INSERT INTO mises 
                        (mise2, resultat2, equipe2, cote2, id_utilisateur, id_match, datemise)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        mise2_decimal, resultat2, equipe2, cote2, utilisateur, id_match, datemise
                    ))
           


    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('user.espace_utilisateur'))

