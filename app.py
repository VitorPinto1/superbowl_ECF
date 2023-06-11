from flask import Flask, render_template, redirect, session, request, url_for
from flask_bootstrap import Bootstrap
from datetime import datetime
import json



app = Flask(__name__)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True

app.secret_key='Pocholo123456'



bootstrap = Bootstrap(app)



@app.route('/')

def index():
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y")
    return render_template('index.html', current_date=formatted_date)

class Matchs:
    def __init__(self, equipe1, equipe2, jour, debut, fin, statut, score, meteo, joueurs, cote1, cote2, commentaires):
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.jour = jour
        self.debut = debut
        self.fin = fin
        self.statut = statut
        self.score = score
        self.meteo = meteo
        self.joueurs = joueurs
        self.cote1 = cote1
        self.cote2 = cote2
        self.commentaires = commentaires


def obtenir_matchs():
     matchs = [
        Matchs('Kansas City Chiefs', 'Dallas Cowboys', '23/05', '09:00', '11:00', 'En cours','4-2', 'soleil','pepe', '500$', '200$' , 'el mejor jugador'),
        Matchs('New England Patriots', 'Green Bay Packers', '24/05', '08:00', '10:00', 'Terminé','0-3', 'pluie', 'batista', '400$','200$', 'que rule'),
        Matchs('Pittsburgh Steelers', 'San Francisco 49ers', '29/05', '10:00', '12:00', 'À venir','', 'horage', 'ronaldinho', '2000$','200$', 'El gaucho')
        ]
     return matchs


@app.route('/visualiser_matchs')
def visualiser_matchs():
    matchs = obtenir_matchs()
    return render_template('visualiser_matchs.html', matchs = matchs)


@app.route('/store_in_session', methods=['POST'])
def store_in_session():
    session['equipe1'] = request.form.get('equipe1')
    session['equipe2'] = request.form.get('equipe2')
    session['cote1'] = request.form.get('cote1')
    session['cote2'] = request.form.get('cote2')
    return redirect(url_for('miser'))

@app.route('/miser')
def miser():
    equipe1 = session.get('equipe1')
    equipe2 = session.get('equipe2')
    cote1 = session.get('cote1')
    cote2 = session.get('cote2')
    return render_template('miser.html', equipe1=equipe1, equipe2=equipe2, cote1=cote1, cote2=cote2)


@app.route('/parier')
def parier():
    matchs = obtenir_matchs()
    return render_template('parier.html', matchs=matchs)

@app.route('/miser_sur_la_selection', methods=['POST'])
def miser_sur_la_selection():
   
   
    donnees_selectionnees = request.form.get('donnees_selectionnees')
    
    # JSON a objet Python
    matchs_selectionnes = json.loads(donnees_selectionnees)

    equipe1 = request.form.get('equipe1')
    equipe2 = request.form.get('equipe2')
    cote1 = request.form.get('cote1')
    cote2 = request.form.get('cote2')


   
    return render_template('miser_sur_la_selection.html', matchs_selectionnes=matchs_selectionnes, equipe1=equipe1, equipe2=equipe2, cote1=cote1,cote2=cote2)

@app.route('/se_connecter')
def se_connecter():
    return render_template('se_connecter.html')

@app.route('/mot_de_passe_oublie')
def mot_de_passe_oublie():
    return render_template("mot_de_passe_oublie.html")


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


