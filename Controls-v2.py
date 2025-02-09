import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, ceil

def calculate_flight_time(distance, max_velocity, max_acceleration):
    
    time_to_max_velocity = max_velocity / max_acceleration
    distance_to_max_velocity = 0.5 * max_acceleration * time_to_max_velocity**2

    if distance_to_max_velocity >= distance:
        time_to_max_velocity = sqrt(2 * distance / max_acceleration)
        return time_to_max_velocity
    else:
        remaining_distance = distance - distance_to_max_velocity
        cruise_velocity = min(0.8 * max_velocity, max_velocity)
        cruise_time = remaining_distance / cruise_velocity
        total_time = time_to_max_velocity + cruise_time
        return total_time

def plot_missile_path(point1, point2):
    x_values = [point1[0], point2[0]]
    y_values = [point1[1], point2[1]]

    plt.figure(figsize=(8, 8))
    plt.plot(x_values, y_values, marker='o', color='red', label="Missile Path")
    
    plt.title("Missile Path Visualization")
    plt.xlabel("X Coordinate (km)")
    plt.ylabel("Y Coordinate (km)")
    plt.grid(True)
    
    # Setting the grid scale (Currently it is 1 unit = 1 km)
    plt.xticks(range(ceil(max(x_values)) + 1))
    plt.yticks(range(ceil(max(y_values)) + 1))
    
    plt.legend()
    plt.show()

def select_points_on_grid(grid_scale):

    print(f"Select two points on a {grid_scale}x{grid_scale} grid.")
    print(" ")
    
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
        x1, y1 = points_selected[0]
        x2, y2 = points_selected[1]
        
        #Calculating the straight line distance between the two plotted points
        distance_km = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        print(f"Selected Points: {points_selected}")
        print(" ")
        print(f"Calculated Distance: {distance_km:.2f} km")
        print(" ")
    
        return points_selected[0], points_selected[1], distance_km
    

try:
    grid_scale = int(input("Enter grid scale (e.g., maximum x and y values in km): "))
    print(" ")

    point1, point2, range_km = select_points_on_grid(grid_scale)
    
    range_meters = range_km * 1000

    max_velocity = float(input("Enter maximum velocity in m/s: "))
    print(" ")

    max_acceleration = float(input("Enter maximum acceleration in m/s²: "))
    print(" ")

    flight_time = calculate_flight_time(range_meters, max_velocity, max_acceleration)
    
    print(f"Calculated Flight Time: {flight_time:.2f} seconds")
    print(" ")

    plot_missile_path(point1, point2)

except ValueError:
    print("Invalid input! Please enter numeric values.")