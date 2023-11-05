from sys import maxsize
from itertools import permutations

from objects.waypoint import Waypoint
from objects.mission import Mission


"""
This function returns the less energy consuming path for the given waypoints from greedy set cover function.
"""


def travellingSalesmanProblem(
    selected_waypoints: list[Waypoint],
) -> Mission:
    # Initialize the list of vertices
    vertex = []
    s = 0  # starts from the depo
    for i in range(len(selected_waypoints)):
        if i != s:
            vertex.append(i)

    min_path_weight = maxsize
    min_path = None  # Initialize the min_path as None

    next_permutation = permutations(vertex)
    for i in next_permutation:
        current_path_weight = 0
        path = [selected_waypoints[s]]  # Initialize the path with the source vertex
        k = s
        for j in i:
            current_path_weight += selected_waypoints[k].flying_cost
            path.append(selected_waypoints[j])
            k = j
        current_path_weight += selected_waypoints[k].flying_cost

        if current_path_weight < min_path_weight:
            min_path_weight = current_path_weight
            min_path = path

    min_path.append(selected_waypoints[s])

    return Mission(min_path, min_path_weight)
