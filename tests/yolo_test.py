import os
import uuid
import requests

from Drone.Drone import DroneDirection, lock_yaw_move
from Rasyolo.detect import run
from Constants import weight


def func(vehicle):
    print("before capture image ")
    response = requests.get('http://127.0.0.1:8000/camera')
    print(response.text)
    print("After capture image")
    decision = run(weights=weight, source='image.jpg', conf_thres=0.9)
    print('After prediction')
    os.rename('image.jpg', f'pics/{str(uuid.uuid1())}.jpg')
    print('After rename')

    if not decision:
        return 0
        

    # Moving to helipad
    print('Drone is in quadrant', decision[4])
    print("Taken by AI....")
    # forwardLocation = get_location_metres(vehicle.location.global_relative_frame, decision[0], vehicle.heading)
    # backwardLocation = get_location_metres(vehicle.location.global_relative_frame, decision[1], vehicle.heading)
    # rightLocation = get_location_metres(vehicle.location.global_relative_frame, decision[2], vehicle.heading)
    # leftLocation = get_location_metres(vehicle.location.global_relative_frame, decision[3], vehicle.heading)
    # vehicle.simple_goto(forwardLocation, groundspeed=AiSpeed)
    # time.sleep(1)
    # vehicle.simple_goto(backwardLocation, groundspeed=AiSpeed)
    # time.sleep(1)
    # vehicle.simple_goto(rightLocation, groundspeed=AiSpeed)
    # time.sleep(1)
    # vehicle.simple_goto(leftLocation, groundspeed=AiSpeed)
    # time.sleep(1)
    lock_yaw_move(vehicle, direction=DroneDirection.FORWARD,speed=0.5, distance=decision[0])
    lock_yaw_move(vehicle, direction=DroneDirection.BACKWARD,speed=0.5, distance=decision[1])
    lock_yaw_move(vehicle, direction=DroneDirection.RIGHT,speed=0.5, distance=decision[2])
    lock_yaw_move(vehicle, direction=DroneDirection.LEFT,speed=0.5, distance=decision[3])
    return decision[:4]
