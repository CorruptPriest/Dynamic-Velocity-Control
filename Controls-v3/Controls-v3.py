import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt, ceil, atan2

def calculate_flight_time(distance, max_velocity, max_acceleration, max_altitude, cruise_altitude):


    # Here the cruise speed is 80% of max_velocity
    cruise_speed = 0.8 * max_velocity

    # Phase 1: Ascent to max altitude
    time_to_max_velocity = max_velocity / max_acceleration
    distance_to_max_velocity = 0.5 * max_acceleration * time_to_max_velocity**2

    time_to_max_altitude = sqrt(2 * max_altitude / max_acceleration)  
    distance_to_max_altitude = 0.5 * max_acceleration * time_to_max_altitude**2  

    # Phase 2: Transition to cruise altitude and cruise
    horizontal_distance_at_max_altitude = distance - distance_to_max_altitude
    cruise_time = horizontal_distance_at_max_altitude / cruise_speed

    # Phase 3: Descent from cruise altitude to 0 meters
    descent_time = cruise_altitude / (0.2 * cruise_speed)  

    # Total flight time
    total_time = time_to_max_altitude + cruise_time + descent_time

    return total_time


def plot_missile_path(point1, point2, max_altitude, cruise_altitude, flight_time, max_velocity, max_acceleration):
    """
    Plots the missile's 3D path, including ascent to max altitude, cruise, and descent phases.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    x1, y1 = point1
    x2, y2 = point2

    horizontal_distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)

    cruise_speed = 0.8 * max_velocity

    num_points = 100
    t = np.linspace(0, 1, num_points)

    # Trajectory calculation
    z = np.zeros(num_points)
    x = np.zeros(num_points)
    y = np.zeros(num_points)

    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t

    t_ascent = 0.25
    t_cruise = 0.50


    z[t < t_ascent] = (max_altitude) * (t[t < t_ascent] / t_ascent) #Ascent to max altitude
    z[(t >= t_ascent) & (t < t_cruise)] = max_altitude - (max_altitude - cruise_altitude) * ((t[(t >= t_ascent) & (t < t_cruise)] - t_ascent) / (t_cruise - t_ascent)) #Descent from max altitude to cruise altitude
    z[t >= t_cruise] = cruise_altitude - (cruise_altitude) * ((t[t >= t_cruise] - t_cruise) / (1-t_cruise)) #Descent from cruise altitude to 0


    ax.plot(x, y, z, color='red', label="Missile Path")

    ax.set_xlabel("X Coordinate (km)")
    ax.set_ylabel("Y Coordinate (km)")
    ax.set_zlabel("Altitude (km)")
    ax.set_title("Missile Trajectory in 3D")

    # Setting grid scale
    max_range = max(max(x), max(y))
    ax.set_xlim([0, max_range])
    ax.set_ylim([0, max_range])
    ax.set_zlim([0, max_altitude])

    ax.legend()
    plt.show()


def select_points_on_grid(grid_scale):

    print(f"Select two points on a {grid_scale}x{grid_scale} grid.")

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.set_xlim(0, grid_scale)
    ax.set_ylim(0, grid_scale)

    ax.set_title("Select Two Points on the Grid")

    points_selected = []

    def onclick(event):
        if len(points_selected) < 2:
            points_selected.append((event.xdata, event.ydata))
            ax.plot(event.xdata, event.ydata, 'ro')
            fig.canvas.draw()
            if len(points_selected) == 2:
                plt.close(fig)

    fig.canvas.mpl_connect('button_press_event', onclick)

    ax.grid(True)

    plt.show()

    if len(points_selected) == 2:
        point1 = points_selected[0]
        point2 = points_selected[1]
        x1, y1 = point1
        x2, y2 = point2

        # Calculating distance between the two points
        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)

        print(f"Selected Points: {point1}, {point2}")
        print(f"Calculated Distance: {distance:.2f} km")

        return point1, point2, distance


try:
    grid_scale = int(input("Enter grid scale (e.g., maximum x and y values in km): "))

    # User selects two points on the grid
    point1, point2, range_km = select_points_on_grid(grid_scale)

    # Input altitude parameters
    max_altitude = float(input("Enter maximum altitude in km: "))
    cruise_altitude = float(input("Enter cruise altitude in km: "))

    # Input other parameters from user
    max_velocity = float(input("Enter maximum velocity in m/s: "))
    max_acceleration = float(input("Enter maximum acceleration in m/s²: "))

    # Convert distances from km to meters for calculations
    range_meters = range_km * 1000
    max_altitude_meters = max_altitude * 1000
    cruise_altitude_meters = cruise_altitude * 1000

    # Calculate flight time
    flight_time = calculate_flight_time(range_meters, max_velocity, max_acceleration, max_altitude_meters, cruise_altitude_meters)

    print(f"Calculated Flight Time: {flight_time:.2f} seconds")

    # Plot missile path
    plot_missile_path(point1, point2, max_altitude, cruise_altitude, flight_time, max_velocity, max_acceleration)

except ValueError:
    print("Invalid input! Please enter numeric values.")