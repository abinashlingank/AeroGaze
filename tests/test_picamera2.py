from picamera2 import Picamera2
from Camera.Camera import capture_image


camera = Picamera2()
capture_image('image3.jpg', camera)
