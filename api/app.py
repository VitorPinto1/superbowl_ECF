import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.config import *



env = os.getenv('FLASK_ENV', 'development')

dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path)

os.environ['FLASK_DEBUG'] = '0'


app = Flask(__name__, static_folder='../static', static_url_path='/static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


app.config['MYSQL_DATABASE_HOST'] = 'mysql-1afb9ef7-staniaprojets-ffa9.j.aivencloud.com'
app.config['MYSQL_DATABASE_PORT'] = 24978
app.config['MYSQL_DATABASE_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = 'defaultdb'

mysql = MySQL(app)
app.config


mysql.init_app(app)

bootstrap = Bootstrap(app)

from paris.paris import paris_bp
from match.match import match_bp
from admin.admin import admin_bp
from user.user import user_bp
from connexion.connexion import connexion_bp

app.register_blueprint(paris_bp, url_prefix='/paris')
app.register_blueprint(match_bp, url_prefix='/match')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user' )
app.register_blueprint(connexion_bp, url_prefix='/connexion')

@app.context_processor
def inject_user():
    return {
        'user_admin': session.get('user_admin', False),
        'id_utilisateur': session.get('id_utilisateur', None)
    }

@app.route('/')
def index():
  now = datetime.now()
  formatted_date = now.strftime("%d/%m/%Y")
  conn = mysql.connect()  
  cursor = conn.cursor()
  cursor.execute("SELECT CURDATE()")
  current_date = cursor.fetchone()[0]

  # Obtenir les matchs de la date actuelle
  cursor.execute('''
    SELECT m.*, e1.logo AS logo_equipe1, e2.logo AS logo_equipe2
    FROM matchs m
    JOIN equipes e1 ON m.equipe1 = e1.nom_equipe
    JOIN equipes e2 ON m.equipe2 = e2.nom_equipe
    WHERE m.jour = %s;
  ''', (current_date,))
  matches = cursor.fetchall()
  
  cursor.close()
  conn.close()


  return render_template('index.html', current_date=formatted_date, matches = matches)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)