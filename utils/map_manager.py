import json, os
from objects.sensor import Sensor
from objects.waypoint import Waypoint
import dearpygui.dearpygui as dpg


class MapManager:
    def __init__(self, sensor_list, waypoint_list):
        self.sensor_list = sensor_list
        self.waypoint_list = waypoint_list

        with dpg.window(label="Save/Load", width=200, height=100, pos=(10, 10)):
            file_name = dpg.add_input_text(label="File Name", default_value="map.json")
            dpg.add_button(
                label="Save",
                callback=lambda: self.save_map_to_file(
                    filename=dpg.get_value(file_name)
                ),
            )
            selected_file = dpg.add_listbox(
                label="Select File",
                items=[file for file in os.listdir() if file.endswith(".json")],
                num_items=3,
                callback=lambda: dpg.set_value(file_name, dpg.get_value(selected_file)),
            )
            dpg.add_button(
                label="Load", callback=lambda: self.load_map_from_file("map.json")
            )

    def save_map_to_file(self, filename):
        sensor_list_dict = [sensor.to_dict() for sensor in self.sensor_list]
        waypoint_list_dict = [waypoint.to_dict() for waypoint in self.waypoint_list]

        with open(filename, "w") as f:
            json.dump({"sensors": sensor_list_dict, "waypoints": waypoint_list_dict}, f)

    def load_map_from_file(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)

        self.sensor_list = [Sensor(**sensor) for sensor in data["sensors"]]
        self.waypoint_list = [
            Waypoint(
                name=waypoint["name"],
                x=waypoint["x"],
                y=waypoint["y"],
                reachable_sensors=[
                    Sensor(**sensor) for sensor in waypoint["reachable_sensors"]
                ],
                flying_cost=waypoint["flying_cost"],
                radius=waypoint.get("radius", 100),
            )
            for waypoint in data["waypoints"]
        ]
