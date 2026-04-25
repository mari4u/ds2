from locust import HttpUser,task,between

class TaskUser(HttpUser):
    wait_time=between(1,2)
    @task
    def create_task(a):
        a.client.post("/tasks/",json={"title":"Load Test","description":"Testing","status":"pending","priority":1})
    @task
    def get_tasks(a):
        a.client.get("/tasks/")
    @task
    def update_task(a):
        a.client.put("/tasks/1",json={"title":"Updated","description":"Updated","status":"completed","priority":2})
    @task
    def delete_task(a):
        a.client.delete("/tasks/1")