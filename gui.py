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
from algorithms.mre import MRE
from algorithms.mrs import MRS

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

w1 = Waypoint("w1", 100, 100, sensor_list, 10)
w2 = Waypoint("w2", 200, 200, sensor_list, 15)
waypoint_list = [w1, w2]

themeManager = ThemeManager()


def redraw_simulation():
    graphics.draw_simulation(sensorHandler.sensor_list, waypointHandler.waypoint_list)


sensorHandler = SensorHandler(sensor_list)
sensorHandler.set_redraw_simulation(redraw_simulation)
waypointHandler = WaypointHandler(waypoint_list, sensorHandler.sensor_list)
waypointHandler.set_redraw_simulation(redraw_simulation)

mapManager = MapManager(sensorHandler, waypointHandler)


def start_simulation(sender, data):
    drone = Drone(dpg.get_value(item=energy_c), dpg.get_value(item=storage_c))

    print("The path for the drone:")

    sensors = sensorHandler.sensor_list.copy()
    waypoints = waypointHandler.waypoint_list.copy()

    selected_algorithm = dpg.get_value(item=algorithm_c)

    M = None
    if selected_algorithm == "RSEO":
        M = RSEO(drone, sensors, waypoints)

    elif selected_algorithm == "MRE":
        M = MRE(drone, sensors, waypoints)

    elif selected_algorithm == "MRS":
        M = MRS(drone, sensors, waypoints)

    if M is not None:
        print(M)
        graphics.draw_simulation(
            sensorHandler.sensor_list, waypointHandler.waypoint_list
        )
        graphics.animate_drone_path(drone, M.flying_path)
    else:
        print("No algorithm selected")


window_width = 400
window_height = 100
window_padding = 10

canvas_width = 1500
canvas_height = 1000
canvas_padding = 10

with dpg.handler_registry():
    # Topbar windows
    with dpg.window(
        label="Select Algorithm",
        width=window_width,
        height=window_height,
        pos=(window_padding, window_padding),
    ):
        algorithm_c = dpg.add_radio_button(
            items=["RSEO", "MRE", "MRS"], horizontal=True, default_value="RSEO"
        )
        dpg.add_button(label="Run Simulation", callback=start_simulation)

    # Sidebar windows
    with dpg.window(
        label="Drone parameters",
        width=window_width,
        height=window_height,
        pos=(window_padding, window_height + 2 * window_padding),
    ):
        energy_c = dpg.add_input_int(label="Energy", default_value=100)
        storage_c = dpg.add_input_int(label="Storage", default_value=50)

    sensorHandler.create_add_sensor_window(
        width=window_width,
        height=window_height,
        pos=(
            window_padding,
            window_height + window_height + 3 * window_padding,
        ),
    )
    sensorHandler.create_sensor_list_window(
        width=window_width,
        height=window_height,
        pos=(
            window_padding,
            window_height + 2 * window_height + 4 * window_padding,
        ),
    )

    waypointHandler.create_add_waypoint_window(
        width=window_width,
        height=window_height,
        pos=(
            window_padding,
            window_height + 3 * window_height + 5 * window_padding,
        ),
    )
    waypointHandler.create_waypoint_list_window(
        width=window_width,
        height=window_height,
        pos=(
            window_padding,
            window_height + 4 * window_height + 6 * window_padding,
        ),
    )

    with dpg.window(
        label="Simulation",
        width=canvas_width,
        height=canvas_height + 50,
        pos=(window_width + 2 * window_padding, window_padding),
    ) as simulation:
        with dpg.drawlist(
            label="Map",
            width=canvas_width,
            height=canvas_height,
            parent=simulation,
        ) as drawlist:
            graphics = Graphics(drawlist)
            graphics.draw_simulation(sensorHandler.sensor_list, waypoint_list)
            graphics.set_handlers(sensorHandler, waypointHandler)

  

    mapManager.create_window(
        width=window_width,
        height=window_height,
        pos=(
            window_padding,
            window_height + 5 * window_height + 7 * window_padding,
        ),
    )

    themeManager.create_window(
        width=window_width,
        height=window_height,
        pos=(
            window_padding,
            window_height + 6 * window_height + 8 * window_padding,
        ),
    )

    dpg.add_mouse_release_handler(callback=graphics.mouse_release_handler)   
    dpg.add_mouse_drag_handler(callback=graphics.mouse_drag_handler) 


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
