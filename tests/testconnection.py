from dronekit import connect, VehicleMode, LocationGlobalRelative
from Constants import connectionString, baudRate, speed, lAcc, AiSpeed, landingSpeed, altitude, conf, weight
import time

try:
    # Making Connection
    vehicle = connect(connectionString, wait_ready=True, baud=baudRate)
    time.sleep(2)
    print("Vehicle Connected successfully...")
    vehicle.mode = VehicleMode('ALT_HOLD')

except Exception as e:
    print('Error occurred')
    print(e)
