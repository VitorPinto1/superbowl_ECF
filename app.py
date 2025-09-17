import sys
import os

from scheduler.scheduler import scheduler, taches
from api.config import *

def create_app():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    env = os.getenv('FLASK_ENV', 'development')
    dotenv_path = f'.env.{env}'
    load_dotenv(dotenv_path)
    os.environ['FLASK_DEBUG'] = '0'
    app = Flask(
    __name__,
    template_folder='api/templates',
    static_folder='static',
    static_url_path='/static'
    )
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['MAIL_SERVER'] = 'live.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'api'
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
    mongo = PyMongo(app)
    app.extensions['mongo'] = mongo

    mail = Mail(app)
    app.extensions['mail'] = mail
    


   
    
    app.config['MYSQL_DATABASE_HOST'] = 'mysql-1afb9ef7-staniaprojets-ffa9.j.aivencloud.com'
    app.config['MYSQL_DATABASE_PORT'] = 24978
    app.config['MYSQL_DATABASE_USER'] = os.environ.get('MYSQL_USER')
    app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
    app.config['MYSQL_DATABASE_DB'] = 'defaultdb'

    mysql = MySQL(app)
    app.extensions['mysql'] = mysql
    mysql.init_app(app)
    Bootstrap(app)
    scheduler.init_app(app)
    from paris.paris import paris_bp
    from match.match import match_bp
    from admin.admin import admin_bp
    from user.user import user_bp
    from connexion.connexion import connexion_bp
    from records.records import records_bp
    app.register_blueprint(paris_bp, url_prefix='/paris')
    app.register_blueprint(match_bp, url_prefix='/match')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(connexion_bp, url_prefix='/connexion')
    app.register_blueprint(records_bp, url_prefix='/records')
    @app.context_processor
    def inject_user_data():
        data = {
            'user_admin': session.get('user_admin', False),
            'id_utilisateur': session.get('id_utilisateur', None)
        }
        if 'id_utilisateur' in session:
            id_utilisateur = session['id_utilisateur']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE id = %s", (id_utilisateur,))
            result = cursor.fetchone()
            if result is not None:
                role = result[0]
                data['user_admin'] = (role == 'admin')
            cursor.close()
            conn.close()
        return data
    @app.route('/')
    def index():
        # Utiliser l'heure française
        from datetime import timezone, timedelta
        france_tz = timezone(timedelta(hours=2))  # UTC+2 (heure d'été française)
        now_france = datetime.now(france_tz)
        current_date = now_france.date()
        formatted_date = current_date.strftime("%d/%m/%Y")
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, e1.logo AS logo_equipe1, e2.logo AS logo_equipe2 
            FROM matchs m 
            JOIN equipes e1 ON m.equipe1 = e1.nom_equipe 
            JOIN equipes e2 ON m.equipe2 = e2.nom_equipe 
            WHERE m.jour = %s 
            ORDER BY m.debut
            LIMIT 5
        ''', (current_date,))
        matches = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', current_date=formatted_date, matches=matches)
    taches(app)
    scheduler.start()
    return app

def run():
    app = create_app()
    app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    run()
