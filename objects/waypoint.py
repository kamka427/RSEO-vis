from objects.sensor import Sensor


class Waypoint:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        sensor_list: list[Sensor],
        flying_cost: int,
        radius: int = 100,
        hovering_cost: int = 0,
        max_reward: int = 0,
    ):
        self.name = name
        self.x = x
        self.y = y
        ## sensors that are in radius of waypoint
        self.reachable_sensors = [
            sensor
            for sensor in sensor_list
            if (sensor.x - x) ** 2 + (sensor.y - y) ** 2 <= radius**2
        ]
        self.flying_cost = flying_cost
        self.hovering_cost = sum(
            sensor.hovering_cost for sensor in self.reachable_sensors
        )
        self.max_reward = (
            sum(sensor.reward for sensor in self.reachable_sensors)
            if self.reachable_sensors
            else 0
        )
        self.radius = radius
        self.data_size = sum(sensor.data_size for sensor in self.reachable_sensors)

    def __str__(self):
        return f"Waypoint(x={self.x}, y={self.y}, reachable_sensors={self.reachable_sensors}, hovering_cost={self.hovering_cost}, max_reward={self.max_reward})"

    def to_dict(self):
        return {
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "reachable_sensors": [
                sensor.to_dict() for sensor in self.reachable_sensors
            ],
            "flying_cost": self.flying_cost,
            "hovering_cost": self.hovering_cost,
            "max_reward": self.max_reward,
            "radius": self.radius,
        }
