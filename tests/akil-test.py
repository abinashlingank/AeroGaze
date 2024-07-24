import time
import uuid
from dronekit import LocationGlobalRelative, connect, VehicleMode
import os
import requests
from Constants import AiSpeed, connectionString, baudRate,  lAcc, weight
from Drone.Drone import  get_location_metres,  condition_yaw, arm_and_takeoff
from Rasyolo.detect import run


def func(vehicle, height):
    print("before capture image ")
    response = requests.get('http://127.0.0.1:8000/camera')
    print(response.text)
    print("After capture image")
    decision = run(height=height, weights=weight, source='image.jpg', conf_thres=0.9)
    print('After prediction')
    os.rename('image.jpg', f'pics/{str(uuid.uuid1())}.jpg')
    print('After rename')

    if not decision:
        return 0
        

    # Moving to helipad
    print('Drone is in quadrant', decision[4])
    print("Taken by AI....")
    print(decision)
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
    return decision[:4]

def descend(vehicle, final_altitude):
    print("Descending to ", final_altitude)
    cur_loc = vehicle.location.global_relative_frame
    alt = cur_loc.alt
    target_location = LocationGlobalRelative(cur_loc.lat, cur_loc.lon, final_altitude)
    vehicle.simple_goto(target_location, groundspeed=0.5)
    #lock_yaw_move(vehicle, direction=DroneDirection.DOWN, speed=0.5, distance=abs(cur_loc.alt - final_altitude))
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


def main(con_str, baud):
    try:
        print(con_str)
        print("Connecting to the vehicle on: ", con_str)
        vehicle = connect(con_str, wait_ready=True, baud=baud)
        print("Vehicle Connected successfully...")
        arm_and_takeoff(vehicle, 12)

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
        condition_yaw(vehicle, 0)
        
        # Performing the Operation
        if vehicle.mode == VehicleMode("GUIDED"): 
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

            d = func(vehicle, current_altitude+2)
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
        print("Error : ", e)

# Connet to the Vehicle
if __name__ == "__main__":
        main(connectionString, baudRate)
