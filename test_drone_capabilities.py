import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from Constants import connectionString, baudRate, speed, lAcc, AiSpeed, landingSpeed, altitude, conf, weight
from Drone.Drone import arm_and_takeoff, get_location_metres

try:
    # Making Connection
    vehicle = connect(connectionString, wait_ready=True, baud=baudRate)
    print("Vehicle Connected successfully...")

    destlat, destlong = 12.971730433350809,80.04374350577795
    print("Destination coordinates: ", destlat, destlong)

    print('Change vehicle mode')
    vehicle.mode = VehicleMode('GUIDED')
    time.sleep(2)
    print('Vehicle mode: ', vehicle.mode)

    # Taking off
    arm_and_takeoff(vehicle, altitude)

    dest_location = LocationGlobalRelative(destlat, destlong, altitude)
    vehicle.simple_goto(dest_location, groundspeed=speed)
    time.sleep(60)

    print("Landing...")
    vehicle.mode = VehicleMode("LAND")
    time.sleep(5)

    # Triggering actions like dropping..

    # Return to Launching pad
    print("Return to launch...")
    vehicle.mode = VehicleMode("RTL")
    time.sleep(4)

    print("Landed safely...")

except Exception as e:
    print("Error occured", e)
