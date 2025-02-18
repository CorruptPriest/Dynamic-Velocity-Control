import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, radians, sin, cos, atan2
import folium  # For map visualization

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
    """
    Calculate the great-circle distance between two points on the Earth.
    """
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

def calculate_flight_time(distance, max_velocity, max_altitude):
    """
    Simplified flight time calculation.
    """
    ascent_time = sqrt(2 * max_altitude / 9.81)  # Assuming constant acceleration due to gravity
    cruise_time = distance / max_velocity
    descent_time = ascent_time  # Symmetric ascent and descent
    total_time = ascent_time + cruise_time + descent_time
    return total_time

def plot_trajectory_on_map(start_coords, end_coords, max_altitude, target_city):
    """
    Display the flight trajectory on a Folium map.
    """
    # Create a Folium map centered at the starting location
    m = folium.Map(location=start_coords, zoom_start=4)

    # Add markers for the origin and destination cities
    folium.Marker(start_coords, popup="Origin (Bangalore)", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(end_coords, popup=f"Target ({target_city})", icon=folium.Icon(color='red')).add_to(m)

    # Generate intermediate points for the curved trajectory
    num_points = 100
    latitudes = np.linspace(start_coords[0], end_coords[0], num_points)
    longitudes = np.linspace(start_coords[1], end_coords[1], num_points)

    # Simulate altitude using a parabolic function
    altitudes = max_altitude * (1 - (2 * (np.linspace(0, 1, num_points) - 0.5))**2)

    # Combine latitude and longitude into a list of coordinates
    points = list(zip(latitudes, longitudes))

    # Create a PolyLine to represent the trajectory
    folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(m)

    # Save the map to an HTML file
    m.save("flight_trajectory.html")
    print("Flight trajectory map saved to flight_trajectory.html")

def plot_trajectory(start, end, max_altitude, target_city):
    """
    Generate a smooth parabolic 3D trajectory.
    """
    num_points = 1000
    x = np.linspace(0, haversine_distance(start, end), num_points)
    z = max_altitude * (1 - (2 * (np.linspace(0, 1, num_points) - 0.5))**2)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, np.zeros_like(x), z, label="Missile Trajectory", color='blue', linewidth=2)
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Longitude")
    ax.set_zlabel("Altitude (km)")
    ax.legend()

    # Label the points of origin and ending
    ax.scatter(0, 0, 0, color='green', s=100, label="Origin (Bangalore)")
    ax.scatter(haversine_distance(start, end), 0, 0, color='red', s=100, label=f"Target ({target_city})")
    ax.text(0, 0, 0, "Bangalore", color='green')
    ax.text(haversine_distance(start, end), 0, 0, target_city, color='red')

    # Split the trajectory into 9 parts when 10% of the distance is left
    split_idx = int(0.9 * num_points)
    split_x = x[split_idx:]
    split_z = z[split_idx:]

    # Plot the main trajectory
    ax.plot(x[:split_idx], np.zeros_like(x[:split_idx]), z[:split_idx], color='blue', linewidth=2)

    # Generate and plot the split trajectories
    offset = 0.2  # Increased offset for the split trajectories
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                # Skip the center trajectory (original trajectory)
                continue
            offset_x = (i - 1) * offset
            ax.plot(split_x + offset_x, np.zeros_like(split_x), split_z, color='red', linewidth=2)

    # Clean the display grid
    ax.grid(True)

    # Set the viewing angle for better clarity
    ax.view_init(elev=30, azim=60)

    plt.show()

def main():
    start_city = "Bangalore"

    # Interactive city selection
    print("Select a target city from the following list:")
    city_list = list(cities.keys())
    for i, city in enumerate(city_list):
        if city != start_city:
            print(f"{i}. {city}")

    while True:
        try:
            city_index = int(input("Enter the number of the target city: "))
            if 0 <= city_index < len(city_list) and city_list[city_index] != start_city:
                target_city = city_list[city_index]
                break
            else:
                print("Invalid city number selected.")
        except ValueError:
            print("Invalid input! Please enter a number.")

    # Get user inputs with error handling
    while True:
        try:
            max_velocity = float(input("Enter maximum velocity in m/s: "))
            max_altitude = float(input("Enter maximum altitude in km: "))
            break  # Exit loop if inputs are valid
        except ValueError:
            print("Invalid input! Please enter numeric values.")

    start_coords = cities[start_city]
    end_coords = cities[target_city]

    # Haversine distance calculation
    distance = haversine_distance(start_coords, end_coords)
    flight_time = calculate_flight_time(distance, max_velocity, max_altitude)

    print(f"Distance: {distance:.2f} km")
    print(f"Calculated Flight Time: {flight_time:.2f} seconds")

    plot_trajectory(start_coords, end_coords, max_altitude, target_city)

    # Plot trajectory on a Folium map
    plot_trajectory_on_map(start_coords, end_coords, max_altitude, target_city)

if __name__ == "__main__":
    main()