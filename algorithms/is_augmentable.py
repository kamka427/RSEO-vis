from objects.drone import Drone
from objects.waypoint import Waypoint
from objects.mission import Mission


def is_augmentable(M: Mission, p: Waypoint, drone: Drone) -> bool:
    if M is None or p is None:
        return False
    
    # check if depo is reachable

    print(p.flying_cost + p.hovering_cost + M.total_cost + (len(M.flying_path) and M.distance_to_depo(p)))

    if p.flying_cost + p.hovering_cost + M.total_cost + (len(M.flying_path) and M.distance_to_depo(p)) > drone.energy:
        
      

        return False

    if p.data_size + M.data_size > drone.storage:
        return False

    return True
