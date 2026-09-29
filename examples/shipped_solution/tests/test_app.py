from src.app import greet

def test_greet():
    assert greet("Factory") == "Hello, Factory!"
