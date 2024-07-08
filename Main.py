from dronekit import connect, VehicleMode, LocationGlobalRelative
from Constants import connectionString, baudRate, speed, lAcc, AiSpeed, landingSpeed, altitude, conf, weight
from Drone.Drone import arm_and_takeoff, get_location_metres
from Camera.Camera import capture_image
from picamera2 import Picamera2
import uuid
import time
import os
from Rasyolo.detect1 import run
from ultralytics import YOLO


#load the model
model = YOLO(weight)

try:
    # Making Connection
    vehicle = connect(connectionString, wait_ready=True, baud=baudRate)
    print("Vehicle Connected successfully...")

    destlat, destlong = map(float, input().split(","))
    print("Destination coordinates: ", destlat, destlong)
    #destlat, destlong = 12.971730433350809,80.04374350577795

    print('Change vehicle mode')
    vehicle.mode = VehicleMode('GUIDED')
    time.sleep(2)
    print('Vehicle mode: ', vehicle.mode)

    # Taking off
    arm_and_takeoff(vehicle, altitude)

    # Changing to Guided mode
    #if vehicle.mode.name != "GUIDED":
    vehicle.mode = VehicleMode("GUIDED")

    # Going to Destination
    dest_location = LocationGlobalRelative(destlat, destlong, altitude)
    vehicle.simple_goto(dest_location, groundspeed=speed)
    time.sleep(60)
    
    camera = Picamera2()
    start_time = time.time()
    while time.time() - start_time < 100:
        print("before capture image ")
        # Capturing Image in Raspberry Pi
        capture_image("image.jpg", camera)
        print("After capture image")
        # Running Yolo
        decision = run(weight, 'image.jpg', True, conf_thres=0.8)
        if not any(decision):
            print('helipad not detected')
            continue

        # Moving to helipad
        print('Drone is in quadrant', decision[4])
        print("Taken by AI....")
        forwardLocation = get_location_metres(vehicle.location.global_relative_frame, decision[0], vehicle.heading)
        backwardLocation = get_location_metres(vehicle.location.global_relative_frame, decision[1], vehicle.heading)
        rightLocation = get_location_metres(vehicle.location.global_relative_frame, decision[2], vehicle.heading)
        leftLocation = get_location_metres(vehicle.location.global_relative_frame, decision[3], vehicle.heading)
        vehicle.simple_goto(forwardLocation, groundspeed=AiSpeed)
        time.sleep(1)
        vehicle.simple_goto(backwardLocation, groundspeed=AiSpeed)
        time.sleep(1)
        vehicle.simple_goto(rightLocation, groundspeed=AiSpeed)
        time.sleep(1)
        vehicle.simple_goto(leftLocation, groundspeed=AiSpeed)
        time.sleep(1)

        if all(mov < lAcc for mov in decision[:4]):
            print("Correctly Aligned in the Helipad with accuracy", lAcc)
            break

    # Landing
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
    print(f"Error: {e}")

finally:
    try:
        vehicle.close()
    except NameError:
        pass  # Handle the case where vehicle was never initialized
