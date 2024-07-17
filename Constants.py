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
sensorDim = [25.0, 24.0] # sensor dimension (height, width)
imgDim = (1080, 1920) # Image dimension (height, width)

# Conversions
focalLength /= 10
sensorDim[0] /= 10
sensorDim[1] /= 10
height = altitude*100

#Frame Dimensions of Image while getting distance
frame_dim = (1080, 1920)
