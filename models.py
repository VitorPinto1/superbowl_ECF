from app import db

class Equipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    pays = db.Column(db.String(50), nullable=False)
    joueurs = db.relationship('Joueur', backref='equipe', lazy=True)
    

class Joueur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    numero_joueur = db.Column(db.Integer, nullable=False)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe.id'), nullable=False)
    

