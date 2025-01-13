from flask_apscheduler import APScheduler

scheduler = APScheduler()  # Crear una instancia del planificador

def taches():
    """Registrar tareas planificadas aquí."""
    from match.match import generer_matchs_quotidiens  # Importación local para evitar ciclos

    scheduler.add_job(
        id='generer_matchs_quotidiens',
        func=generer_matchs_quotidiens,
        trigger='cron',
        hour=15,  # Configura la hora de ejecución
        minute=51
    )
