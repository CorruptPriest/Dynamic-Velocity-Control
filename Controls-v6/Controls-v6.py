import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, radians, sin, cos, atan2, tan

# Predefined list of cities with their coordinates (latitude, longitude)
cities = {
    "Bangalore": (12.9716, 77.5946),
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6895, 139.6917),
    "Sydney": (-33.8688, 151.2093),
    "Paris": (48.8566, 2.3522),
    "Moscow": (55.7558, 37.6173)
}

def haversine_distance(coord1, coord2):
    # Calculate the great-circle distance between two points on the Earth
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

def calculate_flight_time(distance, max_velocity):
    # Simplified flight time calculation
    time = distance / max_velocity
    return time

def plot_trajectory(start, end, max_altitude, target_city):
    # Generate a smooth 3D trajectory with ascent and descent angles of 30 degrees
    num_points = 1000
    x = np.linspace(start[0], end[0], num_points)
    y = np.linspace(start[1], end[1], num_points)
    
    # Calculate the horizontal distance
    horizontal_distance = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)
    
    # Calculate the ascent and descent distances
    ascent_distance = max_altitude / tan(radians(30))
    cruise_distance = horizontal_distance - 2 * ascent_distance
    
    # Generate the z coordinates
    z = np.zeros(num_points)
    ascent_idx = int(ascent_distance / horizontal_distance * num_points)
    cruise_idx = int((ascent_distance + cruise_distance) / horizontal_distance * num_points)
    
    z[:ascent_idx] = np.linspace(0, max_altitude, ascent_idx)
    z[ascent_idx:cruise_idx] = max_altitude
    z[cruise_idx:] = np.linspace(max_altitude, 0, num_points - cruise_idx)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, label="Missile Trajectory", color='blue')
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Longitude")
    ax.set_zlabel("Altitude (km)")
    ax.legend()

    # Label the points of origin and ending
    ax.scatter(start[0], start[1], 0, color='green', s=100, label="Origin (Bangalore)")
    ax.scatter(end[0], end[1], 0, color='red', s=100, label=f"Target ({target_city})")
    ax.text(start[0], start[1], 0, "Bangalore", color='green')
    ax.text(end[0], end[1], 0, target_city, color='red')

    # Clean the display grid
    ax.grid(False)
    plt.show()

def main():
    start_city = "Bangalore"
    print("Select a target city from the following list:")
    for city in cities:
        if city != start_city:
            print(city)

    target_city = input("Enter the target city: ")
    if target_city not in cities or target_city == start_city:
        print("Invalid city selected.")
        return

    try:
        max_velocity = float(input("Enter maximum velocity in m/s: "))
        max_altitude = float(input("Enter maximum altitude in km: "))
    except ValueError:
        print("Invalid input! Please enter numeric values.")
        return

    start_coords = cities[start_city]
    end_coords = cities[target_city]
    distance = haversine_distance(start_coords, end_coords)
    final_distance = distance + (4 * max_altitude) - 2 * (max_altitude * 1.732)
    flight_time = calculate_flight_time(final_distance, max_velocity)

    print(f"Distance: {final_distance:.2f} km")
    print(f"Calculated Flight Time: {flight_time:.2f} seconds")

    plot_trajectory(start_coords, end_coords, max_altitude, target_city)

if __name__ == "__main__":
    main()