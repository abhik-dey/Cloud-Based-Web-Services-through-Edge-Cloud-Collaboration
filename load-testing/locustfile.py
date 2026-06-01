from locust import HttpUser, task, between

class BotUser(HttpUser):
    wait_time = between(0.001, 0.005)

    @task
    def book(self):
        self.client.post("/book")