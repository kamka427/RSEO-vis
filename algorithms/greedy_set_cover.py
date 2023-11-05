from objects.sensor import Sensor
from objects.waypoint import Waypoint

"""
This function returns the minimum waypoints, that can reach the desired sensors given from the Knapsack function.
"""


def GreedySetCover(X: set[Sensor], waypoints: set[Waypoint]) -> set:
    I = set()  # Initialize the set cover as an empty set

    iteration = 0  # Counter to track the number of iterations

    while X:  # Repeat until every element in X is covered
        iteration += 1

        max_intersection = 0
        selected_waypoint = None

        for waypoint in waypoints:
            Sj = waypoint.reachable_sensors  # Sensors reachable by this waypoint

            # convert both to sets and calculate the intersection
            set_X = set(X)
            set_Sj = set(Sj)

            intersection = set_X & set_Sj  # Calculate the intersection
            if len(intersection) > max_intersection:
                max_intersection = len(intersection)
                selected_waypoint = waypoint

        if selected_waypoint is None:
            break

        if selected_waypoint is not None and max_intersection > 0:
            I.add(
                selected_waypoint
            )  # Include the waypoint with the maximum intersection into the set cover
            reachable_sensors = set(selected_waypoint.reachable_sensors)
            X = [sensor for sensor in X if sensor not in reachable_sensors]

    return list(I)
