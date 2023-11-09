import unittest

from algorithms.mrs import MRS
from objects.sensor import Sensor
from objects.waypoint import Waypoint
from objects.drone import Drone
from objects.mission import Mission
from objects.depo import Depo


class TestMRS(unittest.TestCase):
    def test_empty(self):
        M = MRS(Drone(100, 100), Depo(), [], [])
        mission = Mission(
            [Waypoint("depo", 0, 0, [], 0), Waypoint("depo", 0, 0, [], 0)], 0
        )
        print("---")
        print(M)
        print("---")
        print(mission)
        self.assertTrue(M == mission)

    def test_single_waypoint(self):
        drone = Drone(100, 100)
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        waypoint1 = Waypoint("waypoint1", 10, 10, [sensor1], 10)
        M = MRS(drone, Depo(), [sensor1], [waypoint1])
        mission = Mission(
            [Waypoint("depo", 0, 0, [], 0), waypoint1, Waypoint("depo", 0, 0, [], 0)],
            10,
        )

        self.assertTrue(M == mission)

    def test_two_waypoints(self):
        drone = Drone(100, 100)
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 100, 100, 10)
        waypoint1 = Waypoint("waypoint1", 10, 10, [sensor1, sensor2], 10)
        waypoint2 = Waypoint("waypoint2", 100, 100, [sensor1, sensor2], 10)
        M = MRS(drone, Depo(), [sensor1, sensor2], [waypoint1, waypoint2])
        mission = Mission(
            [
                Waypoint("depo", 0, 0, [], 0),
                waypoint1,
                waypoint2,
                Waypoint("depo", 0, 0, [], 0),
            ],
            20,
        )
        print("----")
        print(M)
        print(mission)
        self.assertTrue(M == mission)

    def test_three_waypoints(self):
        drone = Drone(100, 100)
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 100, 100, 10)
        sensor3 = Sensor("sensor3", 100, 10, 200, 200, 10)
        waypoint1 = Waypoint("waypoint1", 10, 10, [sensor1, sensor2, sensor3], 10)
        waypoint2 = Waypoint("waypoint2", 100, 100, [sensor1, sensor2, sensor3], 10)
        waypoint3 = Waypoint("waypoint3", 200, 200, [sensor1, sensor2, sensor3], 10)
        M = MRS(drone, Depo(), [sensor1, sensor2, sensor3], [waypoint1, waypoint2, waypoint3])
        mission = Mission(
            [
                Waypoint("depo", 0, 0, [], 0),
                waypoint3,
                waypoint1,
                waypoint2,
                Waypoint("depo", 0, 0, [], 0),
            ],
            30,
        )
        print("----")
        print(M)
        print(mission)
        self.assertTrue(M == mission)
