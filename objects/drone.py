from objects.waypoint import Waypoint
import math


class Drone:
    def __init__(self, energy: int, storage: int):
        self.energy = energy
        self.storage = storage
        self.x: float = 0
        self.y: float = 0

    def __str__(self):
        return f"Drone(energy={self.energy}, storage={self.storage}, x={self.x}, y={self.y})"

    def flying_cost_to_waypoint(self, waypoint: Waypoint) -> int:
        return int(
            math.sqrt((self.x - waypoint.x) ** 2 + (self.y - waypoint.y) ** 2) / 10
        )
