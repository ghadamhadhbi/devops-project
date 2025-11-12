from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import logging
import time
import uuid
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])

# FastAPI app
app = FastAPI(title="Task Management API", version="1.0.0")

# In-memory task storage
tasks_db = {}
task_counter = 0

# Pydantic models
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskResponse(Task):
    id: int
    created_at: str

# Middleware for logging and metrics
@app.middleware("http")
async def log_and_metrics(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    request.state.trace_id = trace_id
    start_time = time.time()
    
    logger.info(f"[{trace_id}] {request.method} {request.url.path} - Request started")
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=response.status_code).inc()
    REQUEST_DURATION.labels(method=request.method, endpoint=request.url.path).observe(duration)
    
    logger.info(f"[{trace_id}] {request.method} {request.url.path} - Status: {response.status_code} - Duration: {duration:.3f}s")
    
    return response

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Get all tasks
@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    logger.info(f"Fetching all tasks. Total count: {len(tasks_db)}")
    return list(tasks_db.values())

# Create a new task
@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: Task):
    global task_counter
    task_counter += 1
    
    new_task = TaskResponse(
        id=task_counter,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=datetime.now().isoformat()
    )
    
    tasks_db[task_counter] = new_task
    logger.info(f"Created task with ID: {task_counter}, Title: {task.title}")
    
    return new_task

# Get a specific task
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    if task_id not in tasks_db:
        logger.warning(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    
    logger.info(f"Fetched task with ID: {task_id}")
    return tasks_db[task_id]

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks_db:
        logger.warning(f"Attempted to delete non-existent task with ID: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    
    deleted_task = tasks_db.pop(task_id)
    logger.info(f"Deleted task with ID: {task_id}, Title: {deleted_task.title}")
    
    return {"message": "Task deleted successfully", "id": task_id}

# Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type="text/plain")

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Task Management API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "tasks": "/tasks",
            "metrics": "/metrics"
        }
    }