# Drone General
acc = 0.95 # Accuracy Confidence for Drone movement
#connectionString = '192.168.50.69:14550'  # Connection String
connectionString = '192.168.137.237:14550'  # Connection String
#connectionString = '127.0.0.1:14550'  # Connection String
baudRate = 57600 # BaudRate
speed = 1 # Mission Speed in m/s
altitude = 10 # Mission Altitude in meters
landingSpeed = 0.1 #Landing Speed in m/s for soft landing

# AI parameters
lAcc = 0.1 # Landing acuuracy in meters
AiSpeed = 0.1 # AI alignment speed in m/s
conf = 0.8 # AI detection accuracy
weight = "Rasyolo/best.pt" # weights of the model

# Camera
focalLength =  3.6 # focal Length of the camera in mm
sensorDim = [24.0, 25.0] # sensor dimension (width, height)
imgDim = (1920, 1080) # Image dimension (width, height)

# Conversions
focalLength /= 1000
sensorDim[0] /= 1000
sensorDim[1] /= 1000
height = altitude*100

#Frame Dimensions of Image while getting distance
frame_dim = (1920, 1080) # Frame Dimension (width, height)
