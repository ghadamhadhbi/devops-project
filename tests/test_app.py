from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_task():
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"
    assert "id" in response.json()
    assert "created_at" in response.json()

def test_get_all_tasks():
    """Test getting all tasks"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_specific_task():
    """Test getting a specific task"""
    # First create a task
    task_data = {"title": "Specific Task"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Now get it
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_get_nonexistent_task():
    """Test getting a task that doesn't exist"""
    response = client.get("/tasks/99999")
    assert response.status_code == 404

def test_delete_task():
    """Test deleting a task"""
    # First create a task
    task_data = {"title": "Task to Delete"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Now delete it
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    
    # Verify it's gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_metrics_endpoint():
    """Test the Prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text