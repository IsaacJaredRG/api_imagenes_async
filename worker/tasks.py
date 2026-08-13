import time
from celery import Celery

# Initialize Celery app
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def image_processing_dummy(file_name: str):
    print(f"[{file_name}] Starting image processing")
    time.sleep(10)  # Simulate a long-running task
    print(f"[¨{file_name}] Finished image processing")
    return f"Processed image: {file_name}"
