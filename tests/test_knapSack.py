import unittest

from algorithms.knap_sack import knapSack
from objects.sensor import Sensor
from objects.waypoint import Waypoint


class TestKnapSack(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(knapSack([], 0), (0, []))

    def test_single_sensor(self):
        sensor = Sensor("sensor1", 10, 10, 10, 10, 10)
        self.assertEqual(knapSack([sensor], 10), (10, [sensor]))

    def test_single_sensor_not_enough_storage(self):
        sensor = Sensor("sensor1", 10, 10, 10, 10, 10)
        self.assertEqual(knapSack([sensor], 9), (0, []))

    def test_two_sensors(self):
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 15, 15, 10)
        self.assertEqual(knapSack([sensor1, sensor2], 20), (20, [sensor1, sensor2]))

    def test_two_sensors_not_enough_storage(self):
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 15, 15, 10)
        self.assertEqual(knapSack([sensor1, sensor2], 19), (10, [sensor1]))

    def test_two_sensors_not_enough_storage2(self):
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 15, 15, 10)
        self.assertEqual(knapSack([sensor1, sensor2], 18), (10, [sensor1]))

    def test_two_sensors_not_enough_storage3(self):
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 15, 15, 10)
        self.assertEqual(knapSack([sensor1, sensor2], 17), (10, [sensor1]))

    def test_two_sensors_not_enough_storage4(self):
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 15, 15, 10)
        self.assertEqual(knapSack([sensor1, sensor2], 16), (10, [sensor1]))

    def test_two_sensors_not_enough_storage5(self):
        sensor1 = Sensor("sensor1", 10, 10, 10, 10, 10)
        sensor2 = Sensor("sensor2", 10, 10, 15, 15, 10)
        self.assertEqual(knapSack([sensor1, sensor2], 15), (10, [sensor1]))
