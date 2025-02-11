import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt, ceil, atan2

def calculate_flight_time(distance, max_velocity, max_acceleration, max_altitude, cruise_altitude):
    """
    Calculates the flight time based on acceleration and cruising dynamics,
    considering altitude changes.

    Parameters:
        distance (float): Horizontal distance to be traveled in meters.
        max_velocity (float): Maximum allowable velocity in m/s.
        max_acceleration (float): Maximum allowable acceleration in m/s².
        max_altitude (float): Maximum altitude the missile reaches in meters.
        cruise_altitude (float): Altitude at which the missile cruises in meters.

    Returns:
        float: Total flight time in seconds.
    """

    # Define cruise speed as 80% of max_velocity
    cruise_speed = 0.8 * max_velocity

    # Phase 1: Ascent to max altitude
    # Assuming constant acceleration to max velocity
    time_to_max_velocity = max_velocity / max_acceleration
    distance_to_max_velocity = 0.5 * max_acceleration * time_to_max_velocity**2

    # Time to reach max altitude (simplified, assuming vertical ascent)
    time_to_max_altitude = sqrt(2 * max_altitude / max_acceleration)  # Simplified vertical motion equation
    distance_to_max_altitude = 0.5 * max_acceleration * time_to_max_altitude**2  # Distance traveled while ascending

    # Phase 2: Transition to cruise altitude and cruise
    horizontal_distance_at_max_altitude = distance - distance_to_max_altitude
    cruise_time = horizontal_distance_at_max_altitude / cruise_speed

    # Phase 3: Descent from cruise altitude to 0 meters
    descent_time = cruise_altitude / (0.2 * cruise_speed)  # Descent rate is 20% of cruise speed

    # Total flight time
    total_time = time_to_max_altitude + cruise_time + descent_time

    return total_time

def smooth_trajectory(point1, point2, max_altitude, cruise_altitude, num_points=100):
    """
    Calculates a smooth 3D trajectory for the missile, including ascent, hover, transition and cruise.
    """
    x1, y1 = point1
    x2, y2 = point2

    # Time fractions for different phases
    t_ascent = 0.25
    t_hover = 0.05  # 20% of ascent time
    t_transition = 0.5  # 50% for smooth transition
    t_descent = 1.0   # Remaining time for descent

    # Generate time array
    t = np.linspace(0, 1, num_points)

    # Initialize arrays for x, y, z coordinates
    x = np.zeros(num_points)
    y = np.zeros(num_points)
    z = np.zeros(num_points)

    # Calculate x and y coordinates (horizontal trajectory)
    x = (1 - t)**3 * x1 + 3*(1 - t)**2 * t * (x1 + (x2-x1)/3) + 3*(1 - t) * t**2 * (x2 - (x2-x1)/3) + t**3 * x2
    y = (1 - t)**3 * y1 + 3*(1 - t)**2 * t * (y1 + (y2-y1)/3) + 3*(1 - t) * t**2 * (y2 - (y2-y1)/3) + t**3 * y2

    # Adjust horizontal movement during ascent
    x[:int(t_ascent*num_points)] = np.linspace(x1, x1 + 0.2*(x2-x1), int(t_ascent*num_points))
    y[:int(t_ascent*num_points)] = np.linspace(y1, y1 + 0.2*(y2-y1), int(t_ascent*num_points))

    # Calculate z coordinates (altitude)
    ascent_idx = int(t_ascent * num_points)
    hover_idx = int((t_ascent + t_hover) * num_points)
    transition_idx = int((t_ascent + t_hover + t_transition) * num_points)

    # Ascent phase (quadratic curve)
    z[:ascent_idx] = max_altitude * (np.linspace(0, 1, ascent_idx)**2)

    # Hover phase
    z[ascent_idx:hover_idx] = max_altitude

    # Transition phase (smooth transition)
    z[hover_idx:transition_idx] = max_altitude - (max_altitude - cruise_altitude) * (np.linspace(0, 1, transition_idx - hover_idx)**2)

    # Descent phase
    z[transition_idx:] = cruise_altitude * (1 - np.linspace(0, 1, num_points - transition_idx)**2)

    return x, y, z

def plot_missile_path(point1, point2, max_altitude, cruise_altitude, flight_time, max_velocity, max_acceleration):
    """
    Plots the missile's 3D path, including ascent to max altitude, hover, transition, cruise, and descent phases, using smoother curves.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Extract horizontal coordinates
    x1, y1 = point1
    x2, y2 = point2

    # Number of points for trajectory
    num_points = 200

    # Generate smooth trajectory
    x, y, z = smooth_trajectory(point1, point2, max_altitude, cruise_altitude, num_points)

    # Plot the missile path
    ax.plot(x, y, z, color='red', label="Missile Path")

    ax.set_xlabel("X Coordinate (km)")
    ax.set_ylabel("Y Coordinate (km)")
    ax.set_zlabel("Altitude (km)")
    ax.set_title("Missile Trajectory in 3D")

    # Set grid scale
    max_range = max(max(x), max(y))
    ax.set_xlim([0, max_range])
    ax.set_ylim([0, max_range])
    ax.set_zlim([0, max_altitude])

    ax.legend()
    plt.show()

def select_points_on_grid(grid_scale):
    """
    Allows user to select two points on a 2D grid.
    """

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

        # Calculate Euclidean distance between the two points
        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)

        print(f"Selected Points: {point1}, {point2}")
        print(f"Calculated Distance: {distance:.2f} km")

        return point1, point2, distance

# Main program execution
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
