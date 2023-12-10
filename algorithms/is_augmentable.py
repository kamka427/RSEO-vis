from objects.drone import Drone
from objects.waypoint import Waypoint
from objects.mission import Mission

def is_augmentable(M: Mission, p: Waypoint, drone: Drone, depo: Waypoint) -> bool:
    if M is None or p is None:
        return False

    total_energy = p.flying_cost + p.hovering_cost + M.flying_cost + M.hovering_cost
    if len(M.flying_path) > 0:
        total_energy += M.distance_to_depo(depo, p)


    if total_energy > drone.energy:
        print(total_energy, "False")
        return False

    if p.data_size + M.data_size > drone.storage:
        print(total_energy, "False")
        return False

    print(total_energy, "True")
    return True
