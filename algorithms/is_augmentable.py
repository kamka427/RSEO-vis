from objects.drone import Drone
from objects.waypoint import Waypoint
from objects.mission import Mission


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
