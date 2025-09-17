from flask_apscheduler import APScheduler

scheduler = APScheduler()  

def taches(app):
    from match.match import generer_matchs_quotidiens, mettre_a_jour_tous_les_statuts

    @scheduler.task('cron', id='generer_matchs_quotidiens', hour=0, minute=0)
    def generer_matchs_con_contexte():
        with app.app_context(): 
            generer_matchs_quotidiens()

    @scheduler.task('interval', id='maj_statuts_complets', seconds=30)
    def maj_statuts_complets_con_contexte():
        with app.app_context():
            mettre_a_jour_tous_les_statuts()