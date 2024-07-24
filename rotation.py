import math
import time
from dronekit import LocationGlobalRelative

# Earth's radius in meters
EARTH_RADIUS = 6378137.0

def move_right(current_location, distance):
    """
    Move forward by 'distance' meters. The latitude remains constant, only longitude changes.
    """
    delta_longitude = (distance / (EARTH_RADIUS * math.cos(math.radians(current_location.lat)))) * (180 / math.pi)
    new_longitude = current_location.lon + delta_longitude
    return LocationGlobalRelative(current_location.lat, new_longitude, current_location.alt)

def move_left(current_location, distance):
    """
    Move backward by 'distance' meters. The latitude remains constant, only longitude changes.
    """
    delta_longitude = (distance / (EARTH_RADIUS * math.cos(math.radians(current_location.lat)))) * (180 / math.pi)
    new_longitude = current_location.lon - delta_longitude
    return LocationGlobalRelative(current_location.lat, new_longitude, current_location.alt)

def move_forward(current_location, distance):
    """
    Move right by 'distance' meters. The longitude remains constant, only latitude changes.
    """
    delta_latitude = (distance / EARTH_RADIUS) * (180 / math.pi)
    new_latitude = current_location.lat + delta_latitude
    return LocationGlobalRelative(new_latitude, current_location.lon, current_location.alt)

def move_back(current_location, distance):
    """
    Move left by 'distance' meters. The longitude remains constant, only latitude changes.
    """
    delta_latitude = (distance / EARTH_RADIUS) * (180 / math.pi)
    new_latitude = current_location.lat - delta_latitude
    return LocationGlobalRelative(new_latitude, current_location.lon, current_location.alt)

def turn_to_north(vehicle):
    current_heading = vehicle.heading  # Get current heading (0 is north, 90 is east)


    # Turn the vehicle to the calculated angle
    vehicle.simple_goto(vehicle.location.global_relative_frame, heading=0)
    time.sleep(1)

    print("Turned towards North successfully!")

