from fastapi import FastAPI, HTTPException
from Camera.Camera import capture_image
import uvicorn
from picamera2 import Picamera2

app = FastAPI()
camera = Picamera2()
config = camera.create_still_configuration(main={'size': (1920, 1080)})
camera.configure(config)

@app.get('/camera')
async def run(name: str):
    capture_image(name, camera)
    return { 'message': 'Image captured successfully'}

if __name__=='main':
    uvicorn.run(app, host='127.0.0.1', port=8000)
