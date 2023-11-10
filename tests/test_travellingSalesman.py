import unittest
from objects.waypoint import Waypoint
from objects.mission import Mission
from algorithms.travelling_salesman import travellingSalesmanProblem


class TestTravellingSalesmanProblem(unittest.TestCase):
    def test_empty(self):
        M = travellingSalesmanProblem([Waypoint("depo", 0, 0, [], 0)])
        mission = Mission(
            [Waypoint("depo", 0, 0, [], 0), Waypoint("depo", 0, 0, [], 0)], 0
        )

        self.assertTrue(M == mission)

    def test_single_waypoint(self):
        waypoint1 = Waypoint("waypoint1", 10, 10, [], 10)
        M = travellingSalesmanProblem([Waypoint("depo", 0, 0, [], 0), waypoint1])
        mission = Mission(
            [Waypoint("depo", 0, 0, [], 0), waypoint1, Waypoint("depo", 0, 0, [], 0)],
            10,
        )

        self.assertTrue(M == mission)

    def test_two_waypoints(self):
        waypoint1 = Waypoint("waypoint1", 10, 10, [], 10)
        waypoint2 = Waypoint("waypoint2", 10, 10, [], 10)
        M = travellingSalesmanProblem(
            [Waypoint("depo", 0, 0, [], 0), waypoint1, waypoint2]
        )
        mission = Mission(
            [
                Waypoint("depo", 0, 0, [], 0),
                waypoint1,
                waypoint2,
                Waypoint("depo", 0, 0, [], 0),
            ],
            20,
        )

        self.assertTrue(M == mission)

    def test_three_waypoints(self):
        waypoint1 = Waypoint("waypoint1", 10, 10, [], 10)
        waypoint2 = Waypoint("waypoint2", 10, 10, [], 10)
        waypoint3 = Waypoint("waypoint3", 10, 10, [], 10)
        M = travellingSalesmanProblem(
            [Waypoint("depo", 0, 0, [], 0), waypoint1, waypoint2, waypoint3]
        )
        mission = Mission(
            [
                Waypoint("depo", 0, 0, [], 0),
                waypoint1,
                waypoint2,
                waypoint3,
                Waypoint("depo", 0, 0, [], 0),
            ],
            30,
        )

        self.assertTrue(M == mission)

    def test_four_waypoints(self):
        waypoint1 = Waypoint("waypoint1", 10, 10, [], 10)
        waypoint2 = Waypoint("waypoint2", 10, 10, [], 10)
        waypoint3 = Waypoint("waypoint3", 10, 10, [], 10)
        waypoint4 = Waypoint("waypoint4", 10, 10, [], 10)
        M = travellingSalesmanProblem(
            [Waypoint("depo", 0, 0, [], 0), waypoint1, waypoint2, waypoint3, waypoint4]
        )
        mission = Mission(
            [
                Waypoint("depo", 0, 0, [], 0),
                waypoint1,
                waypoint2,
                waypoint3,
                waypoint4,
                Waypoint("depo", 0, 0, [], 0),
            ],
            40,
        )

        self.assertTrue(M == mission)
