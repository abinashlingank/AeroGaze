import time
import traceback
from dronekit import VehicleMode, connect 
from Drone.Drone import north_facing, get_distance_metres 
from Rasyolo.detect import run
from Constants import weight, connectionString, baudRate, lAcc
from Rasyolo.models.common import DetectMultiBackend
from rotation import *
from dronekit import LocationGlobalRelative, connect, VehicleMode
import os
import requests


def goto(vehicle, target_location):
    """
    Commands the drone to go to the target location and waits until it reaches.
    """
    vehicle.simple_goto(target_location)

    while True:
        current_location = vehicle.location.global_relative_frame
        distance = get_distance_metres(current_location, target_location)

        if distance < 0.5:  # Check if distance to target is less than 1 meter
            break
        time.sleep(1)

def func(model,vehicle, height):
    # Turning the drone to north facing
    l = move_forward(vehicle.location.global_relative_frame, 0.001)
    vehicle.simple_goto(l)
    time.sleep(2)
    print("Before condition yaw")
    north_facing(vehicle)
    time.sleep(10)
    print("After condition yaw")

    #decision = run(height=height, source=f'pics/test2/image4.jpg', weights=weight)
   
    # Capture image from the camera
    print("before capture image ")
    response = requests.get('http://127.0.0.1:8000/camera')
    print(response.text)
    print("After capture image")
    decision = run(model, height=height, source='image.jpg', conf_thres=0.8)
    print('After prediction')
    t = time.localtime()
    timestamp = time.strftime('%H_%M_%S', t)
    os.rename('image.jpg', f'pics/image_{height}m_{timestamp}.jpg')
    print('After rename')

    if not decision:
        return 0

    print('Drone moves towards', decision[4])
    print("Taken by AI....")
    print(decision)
    temp_current_location = vehicle.location.global_relative_frame
    forwardLocation = move_forward(temp_current_location, decision[0])
    temp_current_location = forwardLocation
    backwardLocation = move_back(temp_current_location, decision[1])
    temp_current_location = backwardLocation
    rightLocation = move_right(temp_current_location, decision[2])
    temp_current_location = rightLocation
    leftLocation = move_left(temp_current_location, decision[3])
    print("moving Forward", decision[0])
    goto(vehicle, forwardLocation)
    time.sleep(2)
    print("moving Backward", decision[1])
    goto(vehicle, backwardLocation)
    time.sleep(2)
    print("moving Right", decision[2])
    goto(vehicle, rightLocation)
    time.sleep(2)
    print("moving Left", decision[3])
    goto(vehicle, leftLocation)
    time.sleep(2)
    return decision[:4]

def descend(vehicle, final_altitude):
    print("Descending to ", final_altitude)
    cur_loc = vehicle.location.global_relative_frame
    alt = cur_loc.alt
    target_location = LocationGlobalRelative(cur_loc.lat, cur_loc.lon, final_altitude)
    vehicle.simple_goto(target_location, groundspeed=0.5)
    # Wait until the vehicle reaches the target altitude
    while True:
        altitude_difference = abs(vehicle.location.global_relative_frame.alt - final_altitude)
        print(f" Current Altitude: {vehicle.location.global_relative_frame.alt:.2f} meters")
        print(altitude_difference)

        # Break the loop if the target altitude is reached (with a tolerance)
        if altitude_difference < 0.5:
            print("Reached target altitude")
            break
        time.sleep(1)

def lander(vehicle, model):
    try:
        start_detection = 10
        end_detection = 2
        current_altitude = start_detection

        current_mode = vehicle.mode
        print("Current Mode: ", current_mode)
        altitude = vehicle.location.global_relative_frame.alt
        print("Altitude of Vehicle ", altitude)

        # Changing the mode to GUIDED
        vehicle.mode = VehicleMode("GUIDED")
        if vehicle.mode.name != "GUIDED":
            vehicle.mode = VehicleMode("GUIDED")
        
        # Performing the Operation
        if vehicle.mode.name == "GUIDED":
            curent_location = vehicle.location.global_relative_frame
            if altitude <= end_detection:
                print("Drone is at the end of the detection")
                vehicle.mode = VehicleMode("LAND")
                print("Landing!!!")
                return

            print("Reducing altitude!!!")
            if altitude > start_detection:
                print(f"Descending to {start_detection}")
                descend(vehicle, start_detection)
            elif altitude <= start_detection and altitude > end_detection:
                descend(vehicle, current_altitude-2)
                current_altitude -= 2
                print(f"Descending to {current_altitude}")

            d = func(model, vehicle, current_altitude+2)
            if not d:
                print('helipad not detected')
                return
            if all(mov < lAcc for mov in d):
                print("Correctly Aligned in the Helipad with accuracy", lAcc)
                vehicle.mode = VehicleMode("LAND")
                print("MODE:", vehicle.mode.name)
                print("Script Ended")
                return

        else:
            print("Mode is not GUIDED")
            exit(0)

    except Exception as e:
        print(traceback.format_exc())

