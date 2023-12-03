from objects.sensor import Sensor
from objects.waypoint import Waypoint

"""
This function returns the minimum waypoints, that can reach the desired sensors given from the Knapsack function.
"""


def GreedySetCover(X: set[Sensor], waypoints: set[Waypoint]) -> set:
    I = set()  # Initialize the set cover as an empty set
    X = set(X)  # Ensure X is a set

    while X:  # Repeat until every element in X is covered
        max_intersection = 0
        selected_waypoint = None

        for waypoint in waypoints:
            Sj = set(waypoint.reachable_sensors)  # Ensure Sj is a set

            intersection = X & Sj  # Calculate the intersection
            if len(intersection) > max_intersection:
                max_intersection = len(intersection)
                selected_waypoint = waypoint

        if selected_waypoint is None:
            break

        I.add(selected_waypoint)  # Include the waypoint with the maximum intersection into the set cover
        X = X.difference(set(selected_waypoint.reachable_sensors))  # Ensure the argument to difference is a set

    return list(I)