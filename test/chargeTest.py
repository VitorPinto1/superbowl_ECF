from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 5)  # Temps d'attente entre les actions

    @task
    def view_matches(self):
        # Envoyer une requête GET à la page qui liste les matchs
        self.client.get("/visualiser_matchs")