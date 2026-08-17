from ast import Import
import time
from celery import Celery
import os
import PIL.Image as Image
import PIL.ImageEnhance as ImageEnhance

# Initialize Celery app
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def image_processing(file_dir: str):
    print(f"[{file_dir}] Starting image processing")
    # validate the file does exist
    if not os.path.exists(file_dir):
        return{"error": f"File {file_dir} does not exist"}
    
    #prepare the file name and route to save the processed image
    base_name = os.path.basename(file_dir)
    destination_dir = os.path.join("processed_images", f"autumn_{base_name}")
    
    try:
        with Image.open(file_dir) as img:
            img = img.convert("RGB")
            
            #alter the image to make it look like autumn
            
            #increase general contrast
            enchancer_contrast = ImageEnhance.Contrast(img)
            img = enchancer_contrast.enhance(1.15)
            
            #Increase saturation
            enchancer_color = ImageEnhance.Color(img)
            img = enchancer_color.enhance(1.25)
            
            #manipulate the color balance to give a warmer tone
            r, g, b = img.split()
            r = r.point(lambda i: min(int(i*1.1), 255))
            b = b.point(lambda i: int(i*0.85))
            
            #merge the channels back
            img = Image.merge("RGB", (r, g, b))  
            
            #reduce brightness slightly to give a more autumn feel
            enhancer_brihtness = ImageEnhance.Brightness(img)
            final_image = enhancer_brihtness.enhance(0.95)
            
            #save the processed image
            final_image.save(destination_dir, format="JPEG")
        
        print(f"[{file_dir}] Finished image processing")
        return {
            "message": f"Image processed and saved",
            "original_file": file_dir,
            "processed_file": destination_dir
        }
    except Exception as e:
        return {"error": f"failed to process image: {str(e)}"}