from objects.waypoint import Waypoint

class Mission:
    def __init__(self, flying_path: list[Waypoint], flying_cost: int):
        self.flying_path = flying_path
        self.flying_cost = flying_cost
        self.hovering_cost = sum(waypoint.hovering_cost for waypoint in flying_path)
        self.total_cost = self.flying_cost + self.hovering_cost

    def __str__(self):
        path = " -> ".join(
            f"{waypoint.name}({waypoint.x}, {waypoint.y}) Reward: {waypoint.max_reward}"
            for waypoint in self.flying_path
        )
        return f"Mission(flying_path=[{path}], flying_cost={self.flying_cost}, hovering_cost={self.hovering_cost}, total_cost={self.total_cost})"

    def remove_waypoint(self, waypoint: Waypoint):
        if waypoint in self.flying_path:
            self.flying_path.remove(waypoint)
            self.flying_cost -= waypoint.flying_cost
            self.hovering_cost -= waypoint.hovering_cost
            self.total_cost -= waypoint.flying_cost + waypoint.hovering_cost
