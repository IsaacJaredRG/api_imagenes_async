from fastapi import FastAPI, UploadFile, File
from worker.tasks import image_processing
from celery.result import AsyncResult
from worker.tasks import celery_app

app = FastAPI()

# Endpoint to receive an image and send it for processing
@app.post("/process image/")
async def get_image(file: UploadFile = File(...)):
    #change later to save the file in disk
    file_name = file.filename
    task = image_processing.delay(file_name)
    return{
        "message": "Image recived and sent for processing",
        "task_id": task.id,
        "file": file_name
    }

# Endpoint to check the status of a task
@app.get("/task-state/{tarea_id}")
async def consultar_estado(tarea_id: str):
    tarea = AsyncResult(tarea_id, app=celery_app)
    respuesta = {
        "tarea_id": tarea_id,
        "estado": tarea.state, 
    }
    if tarea.state == "SUCCESS":
        respuesta["resultado"] = tarea.result
        
    return respuesta        