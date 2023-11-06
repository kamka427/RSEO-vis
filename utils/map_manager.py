import json, os
from objects.sensor import Sensor
from objects.waypoint import Waypoint
import dearpygui.dearpygui as dpg
from utils.sensor_handler import SensorHandler
from utils.waypoint_handler import WaypointHandler


class MapManager:
    def __init__(self, sensorHandler: SensorHandler, waypointHandler: WaypointHandler):
        self.sensorHandler = sensorHandler
        self.waypointHandler = waypointHandler
        self.selected_file = None

    def save_map_to_file(self, filename):
        sensor_list_dict = [
            sensor.to_dict() for sensor in self.sensorHandler.sensor_list
        ]
        waypoint_list_dict = [
            waypoint.to_dict() for waypoint in self.waypointHandler.waypoint_list
        ]

        with open(filename, "w") as f:
            json.dump({"sensors": sensor_list_dict, "waypoints": waypoint_list_dict}, f)

        # Update the list of files in the load window
        dpg.configure_item(
            item=self.selected_file,
            items=[file for file in os.listdir() if file.endswith(".json")],
        )

    def load_map_from_file(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)

        self.sensorHandler.sensor_list = [
            Sensor(**sensor) for sensor in data["sensors"]
        ]

        self.waypointHandler.waypoint_list = [
            Waypoint(
                name=waypoint["name"],
                x=waypoint["x"],
                y=waypoint["y"],
                sensor_list=self.sensorHandler.sensor_list,
                flying_cost=waypoint["flying_cost"],
                radius=waypoint.get("radius", 100),
                hovering_cost=waypoint.get("hovering_cost", 5),
                max_reward=waypoint.get("max_reward", 0),
            )
            for waypoint in data["waypoints"]
        ]

        print(self.waypointHandler.waypoint_list)
        print("Sensors:")
        for waypoint in self.waypointHandler.waypoint_list:
            for sensor in waypoint.reachable_sensors:
                print(sensor)

        self.sensorHandler.redraw_simulation()
        self.waypointHandler.redraw_simulation()

        return self.sensorHandler.sensor_list, self.waypointHandler.waypoint_list

    def create_window(self, width, height, pos):
        with dpg.window(label="Save/Load", width=width, height=height, pos=pos):
            file_name = dpg.add_input_text(label="File Name", default_value="map.json")
            dpg.add_button(
                label="Save",
                callback=lambda: self.save_map_to_file(
                    filename=dpg.get_value(file_name)
                ),
            )
            self.selected_file = dpg.add_listbox(
                label="Select File",
                items=[file for file in os.listdir() if file.endswith(".json")],
                num_items=3,
                callback=lambda: dpg.set_value(file_name, dpg.get_value(self.selected_file)),
            )
            dpg.add_button(
                label="Load", callback=lambda: self.load_map_from_file(dpg.get_value(self.selected_file) )
            )
