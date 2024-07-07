
from time import sleep
from picamera2 import Picamera2
import sys
sys.path.append("..")
from Constants import focalLength, sensorDim, imgDim
from Constants import flightHeight

def capture_image(file_path, camera):
        # camera.resolution = (width, height)
        # camera.rotation = 180 # If your camera is upside down, you can rotate the image
        
        # Capture an image
    camera.start()
    sleep(2)
    camera.capture_file(file_path)
    print("Image captured successfully!")

def getGSD():
    GSDh =  (flightHeight * sensorDim[0]) / (focalLength * imgDim[0])
    GSDw =  (flightHeight * sensorDim[1]) / (focalLength * imgDim[1])
    return GSDh, GSDw

# print(getGSD())
