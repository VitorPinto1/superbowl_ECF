from flask_apscheduler import APScheduler

scheduler = APScheduler()  

def taches():
    from match.match import generer_matchs_quotidiens  

    scheduler.add_job(
        id='generer_matchs_quotidiens',
        func=generer_matchs_quotidiens,
        trigger='cron',
        hour=0,  
        minute=0
    )
