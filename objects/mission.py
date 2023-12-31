from objects.waypoint import Waypoint
from objects.depo import Depo
import math


class Mission:
    def __init__(self, flying_path: list[Waypoint], flying_cost: int):
        self.flying_path = flying_path
        self.flying_cost = flying_cost
        self.hovering_cost = sum(waypoint.hovering_cost for waypoint in flying_path)
        self.total_cost = self.flying_cost + self.hovering_cost
        self.data_size = sum(waypoint.data_size for waypoint in flying_path)
        self.reward = sum(waypoint.max_reward for waypoint in flying_path)

    def __str__(self):
        path = " -> ".join(
            f"{waypoint.name}({waypoint.x}, {waypoint.y}) Reward: {waypoint.max_reward} Data: {waypoint.data_size} Cost: {waypoint.flying_cost + waypoint.hovering_cost}"
            for waypoint in self.flying_path
        )
        return f"Mission(flying_path=[{path}], flying_cost={self.flying_cost}, hovering_cost={self.hovering_cost}, total_cost={self.total_cost}, data_size={self.data_size})"

    def __eq__(self, other):
        if not isinstance(other, Mission):
            return False

        for i in range(len(self.flying_path)):
            if self.flying_path[i].name != other.flying_path[i].name:
                return False

        if self.flying_cost != other.flying_cost:
            return False

        if self.hovering_cost != other.hovering_cost:
            return False

        if self.total_cost != other.total_cost:
            return False

        return True

    def remove_waypoint(self, waypoint: Waypoint):
        if waypoint in self.flying_path:
            self.flying_path.remove(waypoint)
            self.flying_cost -= waypoint.flying_cost
            self.hovering_cost -= waypoint.hovering_cost
            self.total_cost -= waypoint.flying_cost + waypoint.hovering_cost
            self.data_size -= waypoint.data_size
            self.reward -= waypoint.max_reward

    def add_waypoint(self, waypoint: Waypoint):
        if waypoint not in self.flying_path:
            self.flying_path.append(waypoint)
            self.flying_cost += waypoint.flying_cost
            self.hovering_cost += waypoint.hovering_cost
            self.total_cost += waypoint.flying_cost + waypoint.hovering_cost
            self.data_size += waypoint.data_size
            self.reward += waypoint.max_reward

    def add_depo(self, depo: Depo):
        # add to the beginning of the mission
        w_depo = Waypoint(
            name="depo",
            x=depo.x,
            y=depo.y,
            sensor_list=[],
            flying_cost=0,
            hovering_cost=0,
            max_reward=0,
        )
        self.flying_path.insert(0, w_depo)
        self.flying_path.append(w_depo)


    def distance_to_depo(self, waypoint: Waypoint):
        return int(
            math.sqrt(
                (waypoint.x - self.flying_path[0].x) ** 2
                + (waypoint.y - self.flying_path[0].y) ** 2
            )
            / 10
        )
