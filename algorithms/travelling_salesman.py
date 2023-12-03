from sys import maxsize
from itertools import permutations

from objects.waypoint import Waypoint
from objects.mission import Mission


"""
This function returns the less energy consuming path for the given waypoints from greedy set cover function.
"""



def travellingSalesmanProblem(drone, selected_waypoints):
    print(drone)
    n = len(selected_waypoints)
    
    if n == 0:
        return Mission([], 0)

    visited = [False] * n
    path = [selected_waypoints[0]]
    visited[0] = True
    total_cost = 0

    for _ in range(1, n):
        nearest = -1
        nearest_distance = maxsize
        for i in range(n):
            if not visited[i]:
                temp_distance = drone.flying_cost_to_waypoint(selected_waypoints[i])
                print(temp_distance)
                if temp_distance < nearest_distance:
                    nearest_distance = temp_distance
                    nearest = i
        visited[nearest] = True
        path.append(selected_waypoints[nearest])
        total_cost += nearest_distance
        drone.x = selected_waypoints[nearest].x
        drone.y = selected_waypoints[nearest].y


    # Add cost to return to the starting point
    total_cost += drone.flying_cost_to_waypoint(selected_waypoints[0])
    path.append(selected_waypoints[0])

    return Mission(path, total_cost)
