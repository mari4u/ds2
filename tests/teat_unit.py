import pytest
from src.main import Task

def test_valid_status():
    t=Task(title="Test",description="Desc",status="pending",priority=1)
    assert t.status=="pending"

def test_notvalid_status():
    with pytest.raises(ValueError):
        Task(title="Test",description="Desc",status="WRONG",priority=1)

def test_search_case():
    t="Hello World"
    assert "hello" in t.lower()   

def test_allow_statuses():
    a=["pending","in work","completed"]
    for i in a:
        t=Task(title="A",description="B",status=i,priority=1)
        assert t.status==i 