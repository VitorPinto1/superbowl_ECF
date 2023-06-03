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

@app.route('/visualiser_matchs')
def visualiser_matchs():
    matchs = [
        {'Equipes': 'Equipo A vs Equipo B', 'Jour': '2023-06-01', 'Début': '18:00', 'Fin': '20:00', 'Statut': 'Termine', 'Score': '2-1'},
        {'Equipes': 'Equipo C vs Equipo D', 'Jour': '2023-06-02', 'Début': '19:30', 'Fin': '21:30', 'Statut': 'En Cours', 'Score': '0-0'},
        {'Equipes': 'Equipo E vs Equipo F', 'Jour': '2023-06-03', 'Début': '16:00', 'Fin': '18:00', 'Statut': 'À Venir', 'Score': ''}
    ]
    return render_template('visualiser_matchs.html', matchs = matchs)


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


