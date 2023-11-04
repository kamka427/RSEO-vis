from objects.drone import Drone
from objects.sensor import Sensor
from objects.waypoint import Waypoint
from algorithms.rseo import RSEO


if __name__ == "__main__":
    drone = Drone(100, 50)

    # Sensor attributes: index, name, reward, data_size, x, y, hovering_cost
    p1 = Sensor("p1", 20, 10, 100, 100, 5)
    p2 = Sensor("p2", 10, 20, 200, 200, 10)
    p3 = Sensor("p3", 5, 30, 300, 300, 7)
    p4 = Sensor("p4", 60, 10, 400, 400, 4)
    p5 = Sensor("p5", 100, 20, 500, 500, 5)
    p6 = Sensor("p6", 120, 30, 600, 600, 10)
    p7 = Sensor("p7", 60, 10, 700, 700, 7)
    p8 = Sensor("p8", 100, 20, 800, 800, 4)
    p9 = Sensor("p9", 120, 30, 900, 900, 5)
    p10 = Sensor("p10", 60, 10, 1000, 1000, 7)
    sensor_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]

    # Waypoint attributes: name, x, y, reachable_sensors, flying_cost
    w1 = Waypoint("w1", 100, 100, [p1, p2, p3], 10)
    w2 = Waypoint("w2", 200, 200, [p4, p5, p6], 15)
    w3 = Waypoint("w3", 300, 300, [p7, p8, p9, p10], 20)
    waypoint_list = [w1, w2, w3]

    print("The path for the drone:")
    print(RSEO(drone, sensor_list, waypoint_list))
