from objects.drone import Drone
from objects.sensor import Sensor
from objects.waypoint import Waypoint
from objects.mission import Mission
from objects.depo import Depo

from algorithms.is_augmentable import is_augmentable


def MRS(
    drone: Drone, depo: Depo, sensors: list[Sensor], waypoints: list[Waypoint]
) -> Mission:
    M = Mission([], 0)

    drone1 = Drone(drone.energy, drone.storage)

    while waypoints:
        p = best_waypoint_ratio_reward_to_storage(waypoints, drone1)
        if is_augmentable(M, p, drone1, depo):
            M.add_waypoint(p)
            drone1.fly_to_waypoint(p)

        if p is None:
            break

        waypoints.remove(p)

    M.add_depo(depo)

    M.total_cost += M.distance_to_depo(depo, M.flying_path[-2])
    M.flying_cost += M.distance_to_depo(depo, M.flying_path[-2])
    return M


def best_waypoint_ratio_reward_to_storage(
    waypoints: list[Waypoint], drone: Drone
) -> Waypoint:
    best_ratio = 0
    best_waypoint = None

    for p in waypoints:
        total_reward = p.max_reward
        total_storage = p.data_size

        if total_storage == 0:
            continue

        ratio = total_reward / total_storage

        if ratio > best_ratio:
            best_ratio = ratio
            best_waypoint = p

        # p.flying_cost =  drone.flying_cost_to_waypoint(p)
    return best_waypoint
