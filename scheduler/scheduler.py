from flask_apscheduler import APScheduler

scheduler = APScheduler()  

def taches(app):
    from match.match import generer_matchs_quotidiens, mettre_a_jour_debut_en_cours

    @scheduler.task('cron', id='generer_matchs_quotidiens', hour=0, minute=0)
    def generer_matchs_con_contexte():
        with app.app_context(): 
            generer_matchs_quotidiens()

    @scheduler.task('interval', id='maj_statuts_matchs', seconds=60)
    def maj_statuts_con_contexte():
        with app.app_context():
            mettre_a_jour_debut_en_cours()