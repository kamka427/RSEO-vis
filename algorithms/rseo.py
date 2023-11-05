from algorithms.knap_sack import knapSack
from algorithms.greedy_set_cover import GreedySetCover
from algorithms.travelling_salesman import travellingSalesmanProblem

from objects.drone import Drone
from objects.sensor import Sensor
from objects.waypoint import Waypoint
from objects.mission import Mission


"""
RSEO algorithm
"""


def RSEO(drone: Drone, sensors: list[Sensor], waypoints: list[Waypoint]) -> Mission:
    V_prime = knapSack(sensors, drone.storage)[1]
    P_prime = GreedySetCover(V_prime, waypoints)
    M = travellingSalesmanProblem(P_prime)

    removable_waypoints = [
        waypoint for waypoint in M.flying_path if waypoint.name != "depo"
    ]

    while M.total_cost > drone.energy and M.flying_path:
        print(f"Total cost: {M.total_cost}, Energy: {drone.energy}")
        waypont_with_least_reward = min(
            removable_waypoints, key=lambda waypoint: waypoint.max_reward
        )
        M.remove_waypoint(waypont_with_least_reward)



    return M
