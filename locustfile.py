from locust import HttpUser, task, between

class CounterUser(HttpUser):
    wait_time = between(0.3, 0.5)

    @task(5)
    def get_counter(self):
        self.client.get("/api/counter")

    @task(3)
    def increment_counter(self):
        self.client.post("/api/counter/increment")

    @task(1)
    def decrement_counter(self):
        self.client.post("/api/counter/decrement")

    @task(1)
    def reset_counter(self):
        self.client.post("/api/counter/reset")
