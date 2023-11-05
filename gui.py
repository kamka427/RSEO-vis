import dearpygui.dearpygui as dpg
from objects.sensor import Sensor
from objects.waypoint import Waypoint
from objects.drone import Drone
from algorithms.rseo import RSEO
from utils.theme_manager import ThemeManager
from utils.map_manager import MapManager
from utils.graphics import Graphics

dpg.create_context()
dpg.create_viewport(width=1920, height=1080, title="SDMP Simulation")
dpg.setup_dearpygui()


class SensorHandler:
    def __init__(self, sensor_list):
        with dpg.window(label="Add Sensor", width=320, height=150, pos=(10, 120)):
            self.reward_c = dpg.add_input_int(label="Reward", default_value=100)
            self.data_size_c = dpg.add_input_int(label="Data Size", default_value=10)
            self.x_cord_s_c = dpg.add_input_int(label="X", default_value=100)
            self.y_cord_s_c = dpg.add_input_int(label="Y", default_value=100)
            self.hovering_cost_c = dpg.add_input_int(
                label="Hovering Cost", default_value=5
            )
            dpg.add_button(label="Add Sensor", callback=self.create_sensor)

        with dpg.window(label="Sensor List", width=200, height=100, pos=(10, 10)):
            self.sensor_combo = dpg.add_combo(label="Sensor", items=sensor_list)
            dpg.add_button(label="Delete Sensor", callback=self.delete_sensor)

    def create_sensor(self, sender, data):
        reward = dpg.get_value(self.reward_c)
        data_size = dpg.get_value(self.data_size_c)
        x_cord_s = dpg.get_value(self.x_cord_s_c)
        y_cord_s = dpg.get_value(self.y_cord_s_c)
        hovering_cost = dpg.get_value(self.hovering_cost_c)

        sensor = Sensor("p1", reward, data_size, x_cord_s, y_cord_s, hovering_cost)
        sensor_list.append(sensor)
        print(f"Sensor {sensor} added")

        dpg.configure_item(item=self.sensor_combo, items=sensor_list)
        redraw_simulation(sender, data)
        return sensor_list

    def delete_sensor(self, sender, data):
        selected_sensor_str = dpg.get_value(item=self.sensor_combo)
        for sensor in sensor_list:
            if str(sensor) == selected_sensor_str:
                selected_sensor = sensor
                break
        else:
            print("No sensor selected")
            return

        sensor_list.remove(selected_sensor)
        print(f"Sensor {selected_sensor} removed")

        dpg.configure_item(item=self.sensor_combo, items=sensor_list)
        dpg.set_value(item=self.sensor_combo, value="")

        redraw_simulation(sender, data)
        return sensor_list


class WaypointHandler:
    def __init__(self, waypoint_list):
        with dpg.window(label="Add Waypoint", width=320, height=150, pos=(10, 280)):
            self.x_cord_w_c = dpg.add_input_int(label="X", default_value=100)
            self.y_cord_w_c = dpg.add_input_int(label="Y", default_value=100)
            self.radius_c = dpg.add_input_int(label="Radius", default_value=100)
            self.flying_cost_c = dpg.add_input_int(
                label="Flying Cost", default_value=10
            )
            self.hovering_cost_c = dpg.add_input_int(
                label="Hovering Cost", default_value=5
            )
            dpg.add_button(label="Add Waypoint", callback=self.create_waypoint)

        with dpg.window(label="Waypoint List", width=200, height=100, pos=(10, 440)):
            self.waypoint_combo = dpg.add_combo(label="Waypoint", items=waypoint_list)
            dpg.add_button(label="Delete Waypoint", callback=self.delete_waypoint)

    def create_waypoint(self, sender, data):
        x_cord_w = dpg.get_value(self.x_cord_w_c)
        y_cord_w = dpg.get_value(self.y_cord_w_c)
        radius = dpg.get_value(self.radius_c)
        flying_cost = dpg.get_value(self.flying_cost_c)
        hovering_cost = dpg.get_value(self.hovering_cost_c)

        waypoint = Waypoint(
            "w1", x_cord_w, y_cord_w, [], flying_cost, radius, hovering_cost
        )
        waypoint_list.append(waypoint)
        print(f"Waypoint {waypoint} added")

        dpg.configure_item(item=self.waypoint_combo, items=waypoint_list)
        redraw_simulation(sender, data)
        return waypoint_list

    def delete_waypoint(self, sender, data):
        selected_waypoint_str = dpg.get_value(item=self.waypoint_combo)
        for waypoint in waypoint_list:
            if str(waypoint) == selected_waypoint_str:
                selected_waypoint = waypoint
                break
        else:
            print("No waypoint selected")
            return

        waypoint_list.remove(selected_waypoint)
        print(f"Waypoint {selected_waypoint} removed")

        dpg.configure_item(item=self.waypoint_combo, items=waypoint_list)
        dpg.set_value(item=self.waypoint_combo, value="")

        redraw_simulation(sender, data)
        return waypoint_list


themeManager = ThemeManager()
themeManager.create_theme_selector()


def redraw_simulation(sender, data):
    graphics.draw_simulation(sensor_list, waypoint_list)


p1 = Sensor("p1", 20, 10, 150, 150, 5)
p2 = Sensor("p2", 10, 20, 120, 120, 10)
p3 = Sensor("p3", 5, 30, 200, 200, 7)
p4 = Sensor("p4", 60, 10, 180, 180, 4)
sensor_list = [
    p1,
    p2,
    p3,
    p4,
]

w1 = Waypoint("w1", 100, 100, [p1, p2, p3], 10)
w2 = Waypoint("w2", 200, 200, [p4], 15)
waypoint_list = [w1, w2]

mapManager = MapManager(sensor_list, waypoint_list)
mapManager.create_save_load()

sensorHandler = SensorHandler(sensor_list)
waypointHandler = WaypointHandler(waypoint_list)


def start_simulation(sender, data):
    drone = Drone(dpg.get_value(item=energy_c), dpg.get_value(item=storage_c))

    print("The path for the drone:")
    M = RSEO(drone, sensor_list, waypoint_list)
    print(M)

    graphics.animate_drone_path(drone, M.flying_path)


with dpg.handler_registry():
    with dpg.window(label="Drone parameters", width=200, height=100, pos=(10, 10)):
        energy_c = dpg.add_input_int(label="Energy", default_value=100)
        storage_c = dpg.add_input_int(label="Storage", default_value=50)

    with dpg.window(label="Select Algorithm", width=200, height=100, pos=(10, 760)):
        algorithm_c = dpg.add_radio_button(
            items=["RSEO", "MRE", "MRS"], horizontal=True
        )
        dpg.add_button(label="Run Simulation", callback=start_simulation)

    with dpg.window(
        label="Simulation", width=1550, height=1050, pos=(350, 10)
    ) as simulation:
        with dpg.drawlist(
            label="Map", width=1500, height=1000, parent=simulation
        ) as drawlist:
            graphics = Graphics(drawlist)
            graphics.draw_simulation(sensor_list, waypoint_list)


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
