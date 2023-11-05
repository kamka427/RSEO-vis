import unittest
from algorithms.greedy_set_cover import GreedySetCover
from objects.sensor import Sensor
from objects.waypoint import Waypoint


class TestGreedySetCover(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(GreedySetCover(set(), set()), [])

    def test_single_sensor(self):
        sensor = Sensor("sensor1", 10, 10, 10, 10, 10)
        waypoint = Waypoint("waypoint1", 10, 10, [sensor], 10)
        self.assertEqual(GreedySetCover({sensor}, {waypoint}), [waypoint])

    def test_single_sensor_not_enough_storage(self):
        sensor = Sensor("sensor1", 10, 10, 10, 10, 10)
        waypoint = Waypoint("waypoint1", 10, 10, [sensor], 10)
        self.assertEqual(GreedySetCover({sensor}, {waypoint}), [waypoint])

    def test_two_sensors(self):
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 15, 15, 10)
        waypoint = Waypoint("waypoint1", 10, 10, [sensor1, sensor2], 10)
        self.assertEqual(GreedySetCover({sensor1, sensor2}, {waypoint}), [waypoint])

    def test_two_sensors_not_enough_storage(self):
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 15, 15, 10)
        waypoint = Waypoint("waypoint1", 10, 10, [sensor1, sensor2], 10)
        self.assertEqual(GreedySetCover({sensor1, sensor2}, {waypoint}), [waypoint])

    def test_two_sensors_not_enough_storage2(self):
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 15, 15, 10)
        waypoint = Waypoint("waypoint1", 10, 10, [sensor1, sensor2], 10)
        self.assertEqual(GreedySetCover({sensor1, sensor2}, {waypoint}), [waypoint])

    def test_two_sensors_not_enough_storage3(self):
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 15, 15, 10)
        waypoint = Waypoint("waypoint1", 10, 10, [sensor1, sensor2], 10)
        self.assertEqual(GreedySetCover({sensor1, sensor2}, {waypoint}), [waypoint])
