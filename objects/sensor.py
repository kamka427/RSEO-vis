class Sensor:
    def __init__(
        self,
        name: str,
        reward: int,
        data_size: int,
        x: int,
        y: int,
        hovering_cost: int,
    ):
        self.name = name
        self.reward = reward
        self.data_size = data_size
        self.x = x
        self.y = y
        self.hovering_cost = hovering_cost

    def __str__(self):
        return f"Sensor(name={self.name}, reward={self.reward}, data_size={self.data_size}, x={self.x}, y={self.y}, hovering_cost={self.hovering_cost})"

    def to_dict(self):
        return {
            "name": self.name,
            "reward": self.reward,
            "data_size": self.data_size,
            "x": self.x,
            "y": self.y,
            "hovering_cost": self.hovering_cost,
        }
