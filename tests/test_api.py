from fastapi.testclient import TestClient
from src.main import app,base,eng 
base.metadata.create_all(bind=eng)
client=TestClient(app)

def test_create_task():
    a=client.post("/tasks/",json={"title":"Test","description":"Test desc","status":"pending","priority":1})
    assert a.status_code==200
    assert a.json()["message"]=="task made"

def test_get_tasks():
    a=client.get("/tasks/")
    assert a.status_code==200
    assert isinstance(a.json(),list)

def test_invalid_status():
    a=client.post("/tasks/",json={"title":"Bad","description":"Bad","status":"WRONG","priority":1})
    assert a.status_code==422

def test_not_found():
    a=client.put("/tasks/999",json={"title":"X","description":"X","status":"pending","priority":1})
    assert a.status_code==404

def test_sort_wrong_parametr():
    a=client.get("/tasks/sort/?by=wrong")
    assert a.status_code==400

def test_search():
    client.post("/tasks/",json={"title":"Hello","description":"World","status":"pending","priority":1})
    a=client.get("/tasks/search/?query=hello")
    assert a.status_code==200
    assert len(a.json())>=1

def test_update_success():
    b=client.post("/tasks/",json={"title":"Old","description":"Old","status":"pending","priority":1})
    t=client.get("/tasks/").json()
    tid=t[-1]["id"]
    a=client.put(f"/tasks/{tid}",json={"title":"New","description":"New","status":"completed","priority":2})
    assert a.status_code==200

def test_delete_success():
    b=client.post("/tasks/",json={"title":"Delete","description":"Test","status":"pending","priority":1})
    t=client.get("/tasks/").json()
    tid=t[-1]["id"]
    a=client.delete(f"/tasks/{tid}")
    assert a.status_code==200

def test_sort_title():
    a=client.get("/tasks/sort/?by=title")
    assert a.status_code==200
    assert isinstance(a.json(),list)

def test_sort_status():
    a=client.get("/tasks/sort/?by=status")
    assert a.status_code==200

def test_sort_date():
    a=client.get("/tasks/sort/?by=date")
    assert a.status_code==200

def test_top_tasks():
    a=client.get("/tasks/top/?n=2")
    assert a.status_code==200
    assert isinstance(a.json(),list)

def test_search_empty():
    a=client.get("/tasks/search/?query=zzzzzzz")
    assert a.status_code==200
    assert a.json()==[]