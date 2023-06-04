from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from datetime import datetime



app = Flask(__name__)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True



bootstrap = Bootstrap(app)



@app.route('/')

def index():
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y")
    return render_template('index.html', current_date=formatted_date)

class Matchs:
    def __init__(self, equipe1, equipe2, jour, debut, fin, statut, score, meteo, joueurs, cote, commentaires):
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.jour = jour
        self.debut = debut
        self.fin = fin
        self.statut = statut
        self.score = score
        self.meteo = meteo
        self.joueurs = joueurs
        self.cote = cote
        self.commentaires = commentaires

@app.route('/visualiser_matchs')
def visualiser_matchs():
    matchs = [
        Matchs('Kansas City Chiefs', 'Dallas Cowboys', '23/05', '09:00', '11:00', 'En cours','4-2', 'soleil','pepe', '500$' , 'el mejor jugador'),
        Matchs('New England Patriots', 'Green Bay Packers', '24/05', '08:00', '10:00', 'Termine','0-3', 'pluie', 'batista', '400$', 'que rule'),
        Matchs('Pittsburgh Steelers', 'San Francisco 49ers', '29/05', '10:00', '12:00', 'À venir','', 'horage', 'ronaldinho', '2000$', 'El gaucho')
        ]
    return render_template('visualiser_matchs.html', matchs = matchs)

@app.route('/miser')
def miser():
    return render_template('miser.html')

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


