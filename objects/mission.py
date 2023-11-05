from objects.waypoint import Waypoint


class Mission:
    def __init__(self, flying_path: list[Waypoint], flying_cost: int):
        self.flying_path = flying_path
        self.flying_cost = flying_cost
        self.hovering_cost = sum(waypoint.hovering_cost for waypoint in flying_path)
        self.total_cost = self.flying_cost + self.hovering_cost
        self.data_size = sum(waypoint.data_size for waypoint in flying_path)

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

    def add_waypoint(self, waypoint: Waypoint):
        if waypoint not in self.flying_path:
            self.flying_path.append(waypoint)
            self.flying_cost += waypoint.flying_cost
            self.hovering_cost += waypoint.hovering_cost
            self.total_cost += waypoint.flying_cost + waypoint.hovering_cost

    def add_depo(self):
        # add to the beginning of the mission
        depo = Waypoint(
            name="depo",
            x=0,
            y=0,
            sensor_list=[],
            flying_cost=0,
            hovering_cost=0,
            max_reward=0,
        )
        self.flying_path.insert(0, depo)
        self.flying_path.append(depo)
