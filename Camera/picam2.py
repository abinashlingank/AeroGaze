from Camera import capture_image
import time
from picamera2 import Picamera2

camera = Picamera2()
start_time = time.time()
i = 1
while time.time() - start_time < 100:
	# Capturing Image in Raspberry Pi
	capture_image(f"image{i}.jpg", camera)
	i+=1
