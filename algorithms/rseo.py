from algorithms.knap_sack import knapSack
from algorithms.greedy_set_cover import GreedySetCover
from algorithms.travelling_salesman import travellingSalesmanProblem

from objects.drone import Drone
from objects.sensor import Sensor
from objects.waypoint import Waypoint
from objects.mission import Mission
from objects.depo import Depo


"""
RSEO algorithm
"""


def RSEO(
    drone: Drone, depo: Depo, sensors: list[Sensor], waypoints: list[Waypoint]
) -> Mission:
    V_prime = knapSack(sensors, drone.storage)[1]

    max_from_sensors = sum(sensor.data_size for sensor in V_prime)
    P_prime = GreedySetCover(V_prime, waypoints)
    P_prime.insert(0, Waypoint("depo", depo.x, depo.y, [], 0))
    M = travellingSalesmanProblem(drone, P_prime)

    if not M.data_size < drone.storage:
        M.data_size = max_from_sensors

    removable_waypoints = [
        waypoint for waypoint in M.flying_path if waypoint.name != "depo"
    ]

    sorted_removable_waypoints = sorted(removable_waypoints, key=lambda waypoint: waypoint.max_reward)
    M.total_cost += M.distance_to_depo(M.flying_path[-2])
    M.flying_cost += M.distance_to_depo(M.flying_path[-2])
    distance_to_depo = M.distance_to_depo(M.flying_path[-2])

    while M.total_cost > drone.energy and M.flying_path:
        # Remove the waypoint with the least reward from the sorted list
        if sorted_removable_waypoints:
            waypoint_to_remove = sorted_removable_waypoints.pop(0)
            if waypoint_to_remove == M.flying_path[-2]:
                M.total_cost -= distance_to_depo
                M.flying_cost -= distance_to_depo
                
                
            M.remove_waypoint(waypoint_to_remove)

    return M
