from objects.drone import Drone
from objects.sensor import Sensor
from objects.waypoint import Waypoint
from objects.depo import Depo
from algorithms.rseo import RSEO
from algorithms.mre import MRE
from algorithms.mrs import MRS

if __name__ == "__main__":
    drone = Drone(100, 100)

    # Sensor attributes: index, name, reward, data_size, x, y, hovering_cost
    p1 = Sensor("p1", 20, 10, 150, 150, 5)
    p2 = Sensor("p2", 10, 20, 120, 120, 10)
    p3 = Sensor("p3", 5, 30, 200, 200, 7)
    p4 = Sensor("p4", 60, 10, 180, 180, 4)
    sensor_list = [
        p1,
        p2,
        p3,
        p4,
    ]

    w1 = Waypoint("w1", 100, 100, sensor_list, 10)
    w2 = Waypoint("w2", 200, 200, sensor_list, 15)
    waypoint_list = [w1, w2]

    print("RSEO - The path for the drone:")
    print(RSEO(drone, Depo(), sensor_list.copy(), waypoint_list.copy()))

    print("MRE - The path for the drone:")
    print(MRE(drone, Depo(), sensor_list.copy(), waypoint_list.copy()))

    print("MRS - The path for the drone:")
    print(MRS(drone, Depo(), sensor_list.copy(), waypoint_list.copy()))
