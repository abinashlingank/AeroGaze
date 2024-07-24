def calculate_gsd(altitude, sensor_width, sensor_height, image_width, image_height, focal_length):
    gsd_x = (altitude * sensor_width) / (focal_length * image_width)
    gsd_y = (altitude * sensor_height) / (focal_length * image_height)
    return gsd_x, gsd_y

def calculate_movement_in_meters(image_width, image_height, point_x, point_y, gsd_x, gsd_y):
    # Calculate the center coordinates of the image
    center_x = image_width / 2
    center_y = image_height / 2

    # Calculate the differences (distances to move in pixels)
    move_x_pixels = point_x - center_x
    move_y_pixels = point_y - center_y

    # Convert pixel distances to meters using GSD
    move_x_meters = move_x_pixels * gsd_x
    move_y_meters = move_y_pixels * gsd_y

    return move_x_meters, move_y_meters

# Example usage:
altitude = 1  # Altitude of the drone in meters
sensor_width = 24  # Sensor width in millimeters
sensor_height = 25  # Sensor height in millimeters
image_width = 1920  # Width of the image in pixels
image_height = 1080  # Height of the image in pixels
focal_length = 3.6  # Focal length of the camera in millimeters
point_x = 1500  # X-coordinate of the point in the image
point_y = 600   # Y-coordinate of the point in the image

# Calculate GSD
gsd_x, gsd_y = calculate_gsd(altitude, sensor_width, sensor_height, image_width, image_height, focal_length)

# Calculate movement in meters
move_x_meters, move_y_meters = calculate_movement_in_meters(image_width, image_height, point_x, point_y, gsd_x, gsd_y)

print(f"The drone should move {move_x_meters:.4f} meters in the x direction and {move_y_meters:.4f} meters in the y direction.")


from Rasyolo.getDistance import GetDistance
print(GetDistance(1, ))
