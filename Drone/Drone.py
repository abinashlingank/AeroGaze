import time
import math
from dronekit import VehicleMode, LocationGlobal, LocationGlobalRelative
import sys
sys.path.append("..")
from Constants import acc
from enum import Enum
from pymavlink import mavutil


class DroneDirection(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    UP = 5
    DOWN = 6

def condition_yaw(vehicle, heading, relative=False):
    """
    Send MAV_CMD_CONDITION_YAW message to point the vehicle to a specified heading.
    """
    is_relative = 1 if relative else 0
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target_system, target_component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, # command
        0,       # confirmation
        heading, # param 1: target angle, in degrees
        0,       # param 2: speed (degrees per second)
        1,       # param 3: direction -1 ccw, 1 cw
        is_relative, # param 4: relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    vehicle.send_mavlink(msg)
    vehicle.flush()
    
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
    if direction == DroneDirection.FORWARD:
        send_ned_velocity(vehicle, speed, 0, 0, duration)
    elif direction == DroneDirection.BACKWARD:
        send_ned_velocity(vehicle, -speed, 0, 0, duration)
    elif direction == DroneDirection.LEFT:
        send_ned_velocity(vehicle, 0, -speed, 0, duration)
    elif direction == DroneDirection.RIGHT:
        send_ned_velocity(vehicle, 0, speed, 0, duration)
    elif direction == DroneDirection.DOWN:
        send_ned_velocity(vehicle, 0,0,speed, duration)
    elif direction == DroneDirection.UP:
        send_ned_velocity(vehicle, 0,0,-speed, duration)
    else:
        print("Invalid direction. Choose 'forwards', 'backwards', 'left', or 'right'.")

def arm_and_takeoff(vehicle, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*acc:
            print("Reached target altitude")
            break
        time.sleep(1)

def get_location_metres(original_location, distance, heading):
    earth_radius=6378137.0 #Radius of "spherical" earth
    # Coordinate offsets in radians
    dNorth = distance * math.cos(math.radians(heading))
    dEast = distance * math.sin(math.radians(heading))
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    # New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    if type(original_location) is LocationGlobal:
        targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt)
    else:
        raise Exception("Invalid Location object passed")

    return targetlocation

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
