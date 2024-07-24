from pymavlink import mavutil
from dronekit import connect
import threading
import time
from Constants import baudRate, connectionString, weight

from Rasyolo.detect import *
import Rasyolo.models.common as models
from newmain import lander

the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')
vehicle = connect(connectionString, wait_ready=True)
print("ariv connected")
model = models.DetectMultiBackend(weights=weight,device="cpu", dnn=False, fp16=False)

the_connection.wait_heartbeat()
print("ariv Heartbeat from (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

def set_mode(the_connection, mode):
    print(mode)
    if mode not in the_connection.mode_mapping():
        print('Unknown mode:', mode)
        print('Try:', list(the_connection.mode_mapping().keys()))
        return

    mode_id = the_connection.mode_mapping()[mode]

    the_connection.mav.set_mode_send(
        the_connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)

    ack = False
    while not ack:
        ack_msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
        ack_msg = ack_msg.to_dict()

        if ack_msg['command'] == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
            ack = True
            result = mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description
            print(result)

def get_current_flight_mode(the_connection):
    try:
        msg = the_connection.recv_match(type='HEARTBEAT', blocking=True)
        if msg is not None:
            mode = mavutil.mode_string_v10(msg)  
            return mode

    except Exception as e:
        print(e)

def get_current_altitude(the_connection):
    try:
        msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg is not None:
            altitude = msg.relative_alt / 1000.0  
            return altitude

    except Exception as e:
        print(e)

def get_waypoint_reached_status(the_connection, target_waypoint_index):
    try:
        print("JP entered") 
        current_altitude = get_current_altitude(the_connection)
        while True:
            current_altitude = get_current_altitude(the_connection)
            print("flying_Ariv",current_altitude)        # If altitude is greater than 11 meters

            msg = the_connection.recv_match(type='NAV_CONTROLLER_OUTPUT', blocking=True)
            if msg is not None:
                distance_to_wp = msg.wp_dist  # Distance to the next waypoint in meters
                print(f"Distance to Next Waypoint: {distance_to_wp} m")

            if current_altitude > 10 or distance_to_wp == 0:
                print("Changing mode to GUIDED")
                set_mode(the_connection, 'GUIDED')
                time.sleep(2)
                #subprocess.call(['python3','sample.py'])
                lander(vehicle, model)
                set_mode(the_connection, 'AUTO')

    except Exception as e:
        print(e)

# Run all functions
def main():
    target_waypoint_index = 5  # Set your target waypoint index here

    # Start a thread for waypoint reached status retrieval
    waypoint_thread = threading.Thread(target=get_waypoint_reached_status, args=(the_connection, target_waypoint_index))
    waypoint_thread.start()
    print(get_current_altitude(the_connection))

    # Wait for all threads to complete (they run indefinitely)
    waypoint_thread.join()

if __name__ == "__main__":
    main()
