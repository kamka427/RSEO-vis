import dearpygui.dearpygui as dpg
from objects.sensor import Sensor
from objects.waypoint import Waypoint
from objects.drone import Drone
from algorithms.rseo import RSEO
import time
import math
import dearpygui_ext.themes as themes


dpg.create_context()
dpg.create_viewport(width=1920, height=1080, title="SDMP Simulation")
dpg.setup_dearpygui()


# light_theme = themes.create_theme_imgui_light()
# dark_theme = themes.create_theme_imgui_dark()


# def set_theme(sender, data):
#     if dpg.get_value(sender) == "Light":
#         dpg.bind_theme(light_theme)
#     else:
#         dpg.bind_theme(dark_theme)


# def create_theme_selector():
#     with dpg.window(label="Theme Selector", width=200, height=100, pos=(10, 10)):
#         dpg.add_combo(
#             ["Light", "Dark"], label="Theme", callback=set_theme, default_value="Dark"
#         )

from utils.theming import create_theme_selector

# Call this function in your main function
create_theme_selector()

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


def draw_dashed_circle(center, radius, color, segments=100):
    # Calculate the angle between each segment
    angle_step = 2 * math.pi / segments

    # Calculate the start and end points of each segment
    points = [
        (
            (
                center[0] + math.cos(angle) * radius,
                center[1] + math.sin(angle) * radius,
            ),
            (
                center[0] + math.cos(angle + angle_step) * radius,
                center[1] + math.sin(angle + angle_step) * radius,
            ),
        )
        for angle in [i * angle_step for i in range(segments)]
    ]

    # Draw every other segment to create a dashed effect
    for i in range(0, len(points), 2):
        dpg.draw_line(p1=points[i][0], p2=points[i][1], color=color, parent=drawlist)


def draw_simulation():
    draw_map()
    draw_depo()
    draw_sensors(sensor_list)
    draw_waypoints(waypoint_list)


def create_sensor():
    reward = dpg.get_value(item=reward_c)
    data_size = dpg.get_value(item=data_size_c)
    x_cord = dpg.get_value(item=x_cord_s_c)
    y_cord = dpg.get_value(item=y_cord_s_c)
    hovering_cost = dpg.get_value(item=hovering_cost_c)

    sensor = Sensor("p1", reward, data_size, x_cord, y_cord, hovering_cost)
    sensor_list.append(sensor)

    dpg.configure_item(item=sensor_combo, items=sensor_list)


def create_waypoint():
    x_cord = dpg.get_value(item=x_cord_w_c)
    y_cord = dpg.get_value(item=y_cord_w_c)
    # Reachable Sensors here
    flying_cost = dpg.get_value(item=flying_cost_c)

    waypoint = Waypoint("w1", x_cord, y_cord, [], flying_cost)
    waypoint_list.append(waypoint)

    dpg.configure_item(item=waypoint_combo, items=waypoint_list)


def delete_sensor(sender, data):
    selected_sensor_str = dpg.get_value(item=sensor_combo)
    for sensor in sensor_list:
        if str(sensor) == selected_sensor_str:
            selected_sensor = sensor
            break
    else:
        print("No sensor selected")
        return

    sensor_list.remove(selected_sensor)
    print(f"Sensor {selected_sensor} removed")

    dpg.configure_item(item=sensor_combo, items=sensor_list)
    dpg.set_value(item=sensor_combo, value="")
    draw_simulation()


def delete_waypoint(sender, data):
    selected_waypoint_str = dpg.get_value(item=waypoint_combo)
    for waypoint in waypoint_list:
        if str(waypoint) == selected_waypoint_str:
            selected_waypoint = waypoint
            break
    else:
        print("No waypoint selected")
        return

    waypoint_list.remove(selected_waypoint)
    print(f"Waypoint {selected_waypoint} removed")

    dpg.configure_item(item=waypoint_combo, items=waypoint_list)
    dpg.set_value(item=waypoint_combo, value="")
    draw_simulation()


def start_simulation(sender, data):
    drone = Drone(dpg.get_value(item=energy_c), dpg.get_value(item=storage_c))

    print("The path for the drone:")
    M = RSEO(drone, sensor_list, waypoint_list)
    print(M)

    animate_drone_path(drone, M.flying_path, drawlist)


def draw_map():
    dpg.draw_rectangle(
        pmin=(20, 20), pmax=(1530, 1030), fill=(0, 255, 0, 255), parent=drawlist
    )


def draw_depo():
    dpg.draw_circle(
        center=(1550 / 2, 1050 / 2),
        radius=10,
        color=(128, 128, 128, 255),
        fill=(128, 128, 128, 255),
        parent=drawlist,
    )


def draw_sensors(sensor_list):
    for sensor in sensor_list:
        dpg.draw_circle(
            center=(sensor.x + 1550 / 2, sensor.y + 1050 / 2),
            radius=10,
            color=(0, 0, 0, 255),
            fill=(0, 0, 0, 255),
            parent=drawlist,
        )


def draw_waypoints(waypoint_list):
    for waypoint in waypoint_list:
        # draw a yellow dot
        dpg.draw_circle(
            center=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
            radius=10,
            color=(255, 255, 0, 255),
            fill=(255, 255, 0, 255),
            parent=drawlist,
        )
        draw_dashed_circle(
            center=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
            radius=100,
            color=(0, 0, 255, 255),
        )


with dpg.handler_registry():
    with dpg.window(label="Drone parameters", width=200, height=100, pos=(10, 10)):
        energy_c = dpg.add_input_int(label="Energy", default_value=100)
        storage_c = dpg.add_input_int(label="Storage", default_value=50)

    with dpg.window(label="Add Sensor", width=320, height=150, pos=(10, 120)):
        reward_c = dpg.add_input_int(label="Reward", default_value=100)
        data_size_c = dpg.add_input_int(label="Data Size", default_value=10)
        x_cord_s_c = dpg.add_input_int(label="X", default_value=100)
        y_cord_s_c = dpg.add_input_int(label="Y", default_value=100)
        hovering_cost_c = dpg.add_input_int(label="Hovering Cost", default_value=5)
        dpg.add_button(label="Add Sensor", callback=create_sensor)

    with dpg.window(label="Add Waypoint", width=320, height=150, pos=(10, 280)):
        x_cord_w_c = dpg.add_input_int(label="X", default_value=100)
        y_cord_w_c = dpg.add_input_int(label="Y", default_value=100)
        radius_c = dpg.add_input_int(label="Radius", default_value=100)
        flying_cost_c = dpg.add_input_int(label="Flying Cost", default_value=10)
        hovering_cost_c = dpg.add_input_int(label="Hovering Cost", default_value=5)
        dpg.add_button(label="Add Waypoint", callback=create_waypoint)

    with dpg.window(label="Existing Sensors", width=320, height=150, pos=(10, 440)):
        sensor_combo = dpg.add_combo(label="Select Sensor", items=sensor_list)
        dpg.add_button(label="Delete Sensor", callback=delete_sensor)

    with dpg.window(label="Existing Waypoints", width=320, height=150, pos=(10, 600)):
        waypoint_combo = dpg.add_combo(label="Select Waypoint", items=waypoint_list)
        dpg.add_button(label="Delete Waypoint", callback=delete_waypoint)

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
            draw_simulation()


def animate_drone_path(drone: Drone, waypoints: list[Waypoint], drawlist):
    for waypoint in waypoints:
        print(f"Drone: {drone}")
        print(f"Waypoint: {waypoint}")
        steps: int = max(abs(drone.x - waypoint.x), abs(drone.y - waypoint.y))
        print(f"Steps: {steps}")

        if steps == 0:
            continue

        # Calculate the amount to move in each step using integer division
        dx = round((waypoint.x - drone.x) // steps)
        dy = round((waypoint.y - drone.y) // steps)

        drone_id = dpg.draw_circle(
            parent=drawlist,
            center=(drone.x + 1550 / 2, drone.y + 1050 / 2),
            radius=10,
            color=(255, 255, 255, 255),
            fill=(255, 255, 255, 255),
        )

        arrow_id = dpg.draw_arrow(
            parent=drawlist,
            p2=(drone.x + 1550 / 2, drone.y + 1050 / 2),
            p1=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
            thickness=2,
            color=(0, 0, 0, 255),
        )

        for _ in range(steps):
            # Update the drone's position
            drone.x += dx
            drone.y += dy

            # Draw the drone at its new position
            dpg.configure_item(
                drone_id,
                center=(drone.x + 1550 / 2, drone.y + 1050 / 2),
            )

            dpg.configure_item(
                arrow_id,
                p2=(drone.x + 1550 / 2, drone.y + 1050 / 2),
            )

            # Pause for a short time to create the animation effect
            time.sleep(0.01)

        # Wait the hovering time
        # time.sleep(waypoint.hovering_cost)

        # change back waypoint color to yellow
        dpg.draw_circle(
            center=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
            radius=10,
            color=(255, 255, 0, 255),
            fill=(255, 255, 0, 255),
            parent=drawlist,
        )


import json


def save_map_to_file(sensor_list, waypoint_list, filename):
    sensor_list_dict = [sensor.to_dict() for sensor in sensor_list]
    waypoint_list_dict = [waypoint.to_dict() for waypoint in waypoint_list]

    with open(filename, "w") as f:
        json.dump({"sensors": sensor_list_dict, "waypoints": waypoint_list_dict}, f)


def load_map_from_file(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    sensor_list = [Sensor(**sensor) for sensor in data["sensors"]]
    waypoint_list = [
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

    return sensor_list, waypoint_list


save_map_to_file(sensor_list, waypoint_list, "map.json")

sensor_list1, waypoint_list1 = load_map_from_file("map.json")
for sensor in sensor_list1:
    print(sensor)

for waypoint in waypoint_list1:
    print(waypoint)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
