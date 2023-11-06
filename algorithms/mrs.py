from objects.drone import Drone
from objects.sensor import Sensor
from objects.waypoint import Waypoint
from objects.mission import Mission
from objects.depo import Depo


def MRS(
    drone: Drone, depo: Depo, sensors: list[Sensor], waypoints: list[Waypoint]
) -> Mission:
    M = Mission([], 0)

    while len(waypoints) > 0:
        p = best_waypoint_ratio_reward_to_storage(sensors, waypoints, drone)
        if is_augmentable(M, p, drone):
            M.add_waypoint(p)

        print(f"""p = {p}""")
        if p is None:
            break
        waypoints.remove(p)

    # add depo to the mission
    M.add_depo(depo)

    return M


def best_waypoint_ratio_reward_to_storage(
    sensors: list[Sensor], waypoints: list[Waypoint], drone: Drone
) -> Waypoint:
    best_ratio = 0
    best_waypoint = None

    print(f"Number of waypoints: {len(waypoints)}")
    for p in waypoints:
        if not is_augmentable(None, p, drone):
            continue

        reachable_sensors = p.reachable_sensors
        reachable_sensors = [
            sensor for sensor in reachable_sensors if sensor not in sensors
        ]
        total_reward = p.max_reward
        total_storage = p.data_size

        print(f"Total reward: {total_reward}, Total storage: {total_storage}")

        if total_storage == 0:
            continue

        ratio = total_reward / total_storage

        if ratio > best_ratio:
            best_ratio = ratio
            best_waypoint = p

    return best_waypoint


def is_augmentable(M: Mission, p: Waypoint, drone: Drone) -> bool:
    if M is None:
        return True

    if p is None:
        return False

    if p.flying_cost + p.hovering_cost + M.total_cost > drone.energy:
        return False

    if p.data_size + M.data_size > drone.storage:
        return False

    return True
