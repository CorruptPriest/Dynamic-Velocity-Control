
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sqrt, ceil, atan2, pi

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
    Calculates a smooth 3D trajectory for the missile, including ascent, hover, transition, and cruise.
    """
    x1, y1 = point1
    x2, y2 = point2

    # Time fractions for different phases
    t_ascent = 0.25
    t_hover = 0.05  # 5% of total time
    t_transition = 0.25  # 25% of total time
    t_cruise = 0.45  # 45% of total time

    # Generate time array
    t = np.linspace(0, 1, num_points)

    # Initialize arrays for x, y, z coordinates
    x = np.zeros(num_points)
    y = np.zeros(num_points)
    z = np.zeros(num_points)

    # Calculate x and y coordinates (horizontal trajectory)
    x = (1 - t)**3 * x1 + 3*(1 - t)**2 * t * (x1 + (x2-x1)/3) + 3*(1 - t) * t**2 * (x2 - (x2-x1)/3) + t**3 * x2
    y = (1 - t)**3 * y1 + 3*(1 - t)**2 * t * (y1 + (y2-y1)/3) + 3*(1 - t) * t**2 * (y2 - (y2-y1)/3) + t**3 * y2

    # Define indices for different phases
    ascent_idx = int(t_ascent * num_points)
    hover_idx = int((t_ascent + t_hover) * num_points)
    transition_start_idx = hover_idx
    transition_end_idx = int((t_ascent + t_hover + t_transition) * num_points)
    cruise_start_idx = transition_end_idx
    cruise_end_idx = int((t_ascent + t_hover + t_transition + t_cruise) * num_points)

    # Ascent phase (smooth ascent)
    z[:ascent_idx] = max_altitude * (np.sin(np.linspace(0, np.pi/2, ascent_idx))**2)

    # Hover phase
    z[ascent_idx:hover_idx] = max_altitude

    # Transition phase (smooth transition to cruise altitude)
    z[transition_start_idx:transition_end_idx] = (
        max_altitude -
        (max_altitude - cruise_altitude) *
        (np.sin(np.linspace(0, np.pi/2, transition_end_idx - transition_start_idx))**2)
    )

    # Cruise Phase (Straight Line Movement)
    z[cruise_start_idx:cruise_end_idx] = cruise_altitude
    x[cruise_start_idx:cruise_end_idx] = np.linspace(x[cruise_start_idx], x2, cruise_end_idx - cruise_start_idx)
    y[cruise_start_idx:cruise_end_idx] = np.linspace(y[cruise_start_idx], y2, cruise_end_idx - cruise_start_idx)

    # Descent phase
    z[cruise_end_idx:] = cruise_altitude * (np.cos(np.linspace(0, np.pi/2, num_points - cruise_end_idx))**2)

    return x, y, z

def plot_missile_path(point1, point2, max_altitude, cruise_altitude, flight_time, max_velocity, max_acceleration):
    """
    Plots the missile's 3D path, including ascent to max altitude,
    hovering at that altitude,
    transitioning to cruising altitude,
    and descending towards ground level.
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Extract horizontal coordinates
    x1, y1 = point1
    x2, y2 = point2

    # Number of points for trajectory
    num_points = 100

    # Generate smooth trajectory for the main path
    x_main, y_main, z_main = smooth_trajectory(point1,
                                             point2,
                                             max_altitude,
                                             cruise_altitude,
                                             num_points)

    # Determine splitting point (start of final descent)
    split_index = int(0.75 * num_points)

    # Main Missile Path
    ax.plot(x_main[:split_index], y_main[:split_index], z_main[:split_index], color='red', label="Missile Path (Main)")

    # Offset for the split parts (adjust as needed)
    offset_factor = 0.05
    offset_x = offset_factor * (x2 - x1)
    offset_y = offset_factor * (y2 - y1)

    # Plot the split parts with trajectories that adjoin the main path
    num_splits = 8

    for i in range(num_splits):
        angle = 2 * np.pi * i / num_splits # Evenly spaced angles around a circle
        x_offset = offset_x * np.cos(angle)
        y_offset = offset_y * np.sin(angle)

        # Ensure split trajectories start where main trajectory ends
        x_start = x_main[split_index - 1]
        y_start = y_main[split_index - 1]
        z_start = z_main[split_index - 1]

        x_end = x2 + x_offset
        y_end = y2 + y_offset
        z_end = 0 # Ground level

        # Generate points for split trajectories
        num_points_split = num_points - split_index # Number of points for split trajectories
        t_split = np.linspace(0, 1, num_points_split)
        x_split = np.linspace(x_start, x_end, num_points_split)
        y_split = np.linspace(y_start, y_end, num_points_split)
        z_split = np.linspace(z_start, z_end, num_points_split)

        ax.plot(x_split, y_split, z_split, color='blue', alpha=0.5)

    ax.set_xlabel("X Coordinate (km)")
    ax.set_ylabel("Y Coordinate (km)")
    ax.set_zlabel("Altitude (km)")
    ax.set_title("Missile Trajectory in 3D with Split Parts")

    # Set grid scale
    max_range = max(max(x_main), max(y_main))
    ax_range = 1.1 * max_range
    ax.set_xlim([0, ax_range])
    ax.set_ylim([0, ax_range])
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




#All comments and descriptions were written by Github Copilot. The program was written by me.

