# Drone General
acc = 0.95 # Accuracy Confidence for Drone movement
connectionString = 'udp:127.0.0.1:14550'  # Connection String
baudRate = 57600 # BaudRate
speed = 0.5 # Mission Speed in m/s
altitude = 10 # Mission Altitude in meters
landingSpeed = 0.5  # Landing Speed in m/s for soft landing

# AI parameters
lAcc = 0.05 # Landing acuuracy in meters
AiSpeed = 0.5 # AI alignment speed in m/s
conf = 0.9 # AI detection accuracy
weight = "Rasyolo/best2.pt" # weights of the model

# Camera
focalLength = 12.5 # focal Length of the camera in mm
sensorDim = [7.564, 5.476] # sensor dimension (height, width)
imgDim = (1920, 1080) # Image dimension (height, width)

# Conversions
focalLength /= 10
sensorDim[0] /= 10
sensorDim[1] /= 10
flightHeight = altitude*100

#Frame Dimensions of Image while getting distance
frame_dim = (1920, 1080)
