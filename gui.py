import dearpygui.dearpygui as dpg
from objects.sensor import Sensor
from objects.waypoint import Waypoint
from objects.drone import Drone
from algorithms.rseo import RSEO
from utils.theme_manager import ThemeManager
from utils.map_manager import MapManager
from utils.graphics import Graphics
from utils.sensor_handler import SensorHandler
from utils.waypoint_handler import WaypointHandler

dpg.create_context()
dpg.create_viewport(width=1920, height=1080, title="SDMP Simulation")
dpg.setup_dearpygui()


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

themeManager = ThemeManager()
mapManager = MapManager(sensor_list, waypoint_list)


def redraw_simulation():
    graphics.draw_simulation(sensorHandler.sensor_list, waypointHandler.waypoint_list)


sensorHandler = SensorHandler(sensor_list)
sensorHandler.set_redraw_simulation(redraw_simulation)
waypointHandler = WaypointHandler(waypoint_list)
waypointHandler.set_redraw_simulation(redraw_simulation)


def start_simulation(sender, data):
    drone = Drone(dpg.get_value(item=energy_c), dpg.get_value(item=storage_c))

    print("The path for the drone:")
    M = RSEO(drone, sensorHandler.sensor_list, waypoint_list)
    print(M)

    graphics.draw_simulation(sensorHandler.sensor_list, waypoint_list)
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
            graphics.draw_simulation(sensorHandler.sensor_list, waypoint_list)


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
