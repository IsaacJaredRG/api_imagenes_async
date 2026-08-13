from fastapi import FastAPI, UploadFile, File
from worker.tasks import image_processing_dummy

app = FastAPI()

@app.post("/process image/")
async def get_image(file: UploadFile = File(...)):
    #change later to save the file in disk
    file_name = file.filename
    task = image_processing_dummy.delay(file_name)
    return{
        "message": "Image recived and sent for processing",
        "task_id": task.id,
        "file": file_name
    }
