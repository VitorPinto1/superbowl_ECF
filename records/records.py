from flask import Blueprint, render_template, current_app
from connexion.connexion import admin_required

records_bp = Blueprint('records', __name__, template_folder='templates')

@records_bp.route('/records')
def records():
    mongo = current_app.extensions['mongo']
    matchs = list(mongo.db.matchs_year.find().sort("year", 1))
    return render_template('records.html', matchs=matchs)
