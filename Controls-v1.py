import numpy as np
import matplotlib.pyplot as plt

def missile_control(range_target, time_of_flight, max_velocity, max_acceleration):
   
    # Phase 1: Time to reach max velocity
    time_to_max_velocity = max_velocity / max_acceleration
    distance_to_max_velocity = 0.5 * max_acceleration * time_to_max_velocity**2

    # Check if cruise phase is possible
    if distance_to_max_velocity > range_target:
        print("Error: Missile cannot reach maximum velocity within the given range.")
        return None

    # Phase 2: Cruise at 80% of max velocity
    cruise_velocity = 0.8 * max_velocity
    remaining_distance = range_target - distance_to_max_velocity
    cruise_time = remaining_distance / cruise_velocity

    total_time = time_to_max_velocity + cruise_time
    if total_time > time_of_flight:
        print(f"Error: Total flight time ({total_time:.2f} s) exceeds allowed time of flight ({time_of_flight} s).")
        return None

    t_accel = np.linspace(0, time_to_max_velocity, num=50)
    t_cruise = np.linspace(time_to_max_velocity, total_time, num=50)
    distance_accel = 0.5 * max_acceleration * t_accel**2
    velocity_accel = max_acceleration * t_accel
    distance_cruise = distance_to_max_velocity + cruise_velocity * (t_cruise - time_to_max_velocity)
    velocity_cruise = np.full_like(t_cruise, cruise_velocity)
    t_total = np.concatenate((t_accel, t_cruise))
    distance_total = np.concatenate((distance_accel, distance_cruise))
    velocity_total = np.concatenate((velocity_accel, velocity_cruise))

    # Given below are the plot trajectory and velocity profiles on a graph which is generated using Matplotlib library in python
    plt.figure(figsize=(10, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(t_total, distance_total, label="Distance", color='blue')
    plt.title("Missile Trajectory and Velocity Profile")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(t_total, velocity_total, label="Velocity", color='red')
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    print(f"Simulation Successful:")
    print(f"Time to Max Velocity: {time_to_max_velocity:.2f} s")
    print(f"Distance to Max Velocity: {distance_to_max_velocity:.2f} m")
    print(f"Cruise Velocity: {cruise_velocity:.2f} m/s")
    print(f"Total Flight Time: {total_time:.2f} s")

try:
    range_target = float(input("Enter target range in meters: "))
    time_of_flight = float(input("Enter total flight time in seconds: "))
    max_velocity = float(input("Enter maximum velocity in m/s: "))
    max_acceleration = float(input("Enter maximum acceleration in m/s²: "))
    
    missile_control(range_target, time_of_flight, max_velocity, max_acceleration)
except ValueError:
    print("Invalid input! Please enter numeric values.")


# About the method:
# Simulates and dynamically controls the missile's speed with two phases:
# 1. Accelerates to max velocity as quickly as possible.
# 2. Cruises at 80% of max velocity for the remaining distance.(I will add conditions for if the cruise condition is not possible in a future version.)
#
# Parameters:
#     range_target (float): Target distance in meters.
#     time_of_flight (float): Total time of flight in seconds.
#     max_velocity (float): Maximum allowable velocity in m/s.
#     max_acceleration (float): Maximum allowable acceleration in m/s^2.