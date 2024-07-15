from dronekit import connect
from pymavlink import mavutil
import time
from enum import Enum


class DroneDirection(Enum):
    FORWARDS = 1
    BACKWARDS = 2
    LEFT = 3
    RIGHT = 4

def send_ned_velocity(vehicle, vx, vy, vz, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,  # time_boot_ms (not used)
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0, 0, 0,  # x, y, z positions (not used)
        vx, vy, vz,  # x, y, z velocity in m/s
        0, 0, 0,  # x, y, z acceleration (not used)
        0, 0)  # yaw, yaw_rate (not used)
    
    for _ in range(int(duration * 10)):
        vehicle.send_mavlink(msg)
        time.sleep(0.1)

def lock_yaw_move(vehicle, direction, speed, distance):
    """
    Move the drone in a specified direction without changing the yaw angle.

    Parameters:
    vehicle -- Vehicle object
    direction -- 'forwards', 'backwards', 'left', or 'right'
    speed -- speed in m/s
    distance -- distance to move in meters
    """
    duration = distance / speed
    if direction == DroneDirection.FORWARDS:
        send_ned_velocity(vehicle, speed, 0, 0, duration)
    elif direction == DroneDirection.BACKWARDS:
        send_ned_velocity(vehicle, -speed, 0, 0, duration)
    elif direction == DroneDirection.LEFT:
        send_ned_velocity(vehicle, 0, -speed, 0, duration)
    elif direction == DroneDirection.RIGHT:
        send_ned_velocity(vehicle, 0, speed, 0, duration)
    else:
        print("Invalid direction. Choose 'forwards', 'backwards', 'left', or 'right'.")
# Connect to the Vehicle
vehicle = connect('192.168.12.1:14550', wait_ready=True)  # Adjust the connection string as needed

# Make the drone go backwards by 10 meters
lock_yaw_move(vehicle, DroneDirection.LEFT, 1, 10)

# Wait a bit for the movement to complete
time.sleep(20)

# Close vehicle object before exiting script
vehicle.close()
