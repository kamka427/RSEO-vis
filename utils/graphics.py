import math
import dearpygui.dearpygui as dpg
import time
from objects.sensor import Sensor
from objects.waypoint import Waypoint


class Graphics:
    def __init__(self, drawlist):
        self.drawlist = drawlist
        self.dragging = False
        self.dragged_item = None

    def draw_dashed_circle(self, center, radius, color, segments=100):
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

        for i in range(0, len(points), 2):
            dpg.draw_line(
                p1=points[i][0], p2=points[i][1], color=color, parent=self.drawlist
            )

    def draw_map(self):
        dpg.draw_rectangle(
            pmin=(20, 20),
            pmax=(1530, 1030),
            fill=(0, 255, 0, 255),
            parent=self.drawlist,
        )

    def draw_depo(self):
        dpg.draw_circle(
            center=(1550 / 2, 1050 / 2),
            radius=10,
            color=(128, 128, 128, 255),
            fill=(128, 128, 128, 255),
            parent=self.drawlist,
        )

    def draw_sensors(self, sensor_list):
        for sensor in sensor_list:
            dpg.draw_circle(
                center=(sensor.x + 1550 / 2, sensor.y + 1050 / 2),
                radius=10,
                color=(255, 0, 0, 255),
                fill=(255, 0, 0, 255),
                parent=self.drawlist,
            )

    def draw_waypoints(self, waypoint_list):
        for waypoint in waypoint_list:
            # draw a yellow dot
            dpg.draw_circle(
                center=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
                radius=10,
                color=(255, 255, 0, 255),
                fill=(255, 255, 0, 255),
                parent=self.drawlist,
            )
            self.draw_dashed_circle(
                center=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
                radius=100,
                color=(0, 0, 255, 255),
            )

    def animate_drone_path(self, drone, waypoints):
        for waypoint in waypoints:
            steps: int = int(max((abs(drone.x - waypoint.x)), abs(drone.y - waypoint.y)))

            if steps == 0:
                continue

            # Calculate the amount to move in each step using integer division
            dx = ((waypoint.x - drone.x) / steps)
            dy = ((waypoint.y - drone.y) / steps)

            drone_id = dpg.draw_circle(
                parent=self.drawlist,
                center=(drone.x + 1550 / 2, drone.y + 1050 / 2),
                radius=10,
                color=(255, 255, 255, 255),
                fill=(255, 255, 255, 255),
            )

            arrow_id = dpg.draw_arrow(
                parent=self.drawlist,
                p2=(drone.x + 1550 / 2, drone.y + 1050 / 2),
                p1=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
                thickness=2,
                color=(0, 0, 0, 255),
            )

          

            for _ in range(steps):
                # Update the drone's position and round the new position
                drone.x = (drone.x + dx)
                drone.y = (drone.y + dy)

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
            self.clear_drone_waypoint_persistence(waypoint)

    def clear_drone_waypoint_persistence(self, waypoint):
        dpg.draw_circle(
            center=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
            radius=10,
            color=(255, 255, 0, 255),
            fill=(255, 255, 0, 255),
            parent=self.drawlist,
        )

    def draw_simulation(self, sensor_list, waypoint_list):
        self.draw_map()
        self.draw_depo()
        self.draw_sensors(sensor_list)
        self.draw_waypoints(waypoint_list)

    def set_handlers(self, sensorHandler, waypointHandler):
        self.sensorHandler = sensorHandler
        self.waypointHandler = waypointHandler

    def mouse_drag_handler(self, sender):
        HIT_THRESHOLD = 20

        mouse_pos = dpg.get_mouse_pos()
        mouse_pos = (mouse_pos[0] - 1550 / 2, mouse_pos[1] - 1050 / 2)

        # convert to int
        mouse_pos = (int(mouse_pos[0]), int(mouse_pos[1]))

        print(mouse_pos)

        if not self.dragging:
            for sensor in self.sensorHandler.sensor_list:
                if (
                    mouse_pos[0] > sensor.x - HIT_THRESHOLD
                    and mouse_pos[0] < sensor.x + HIT_THRESHOLD
                    and mouse_pos[1] > sensor.y - HIT_THRESHOLD
                    and mouse_pos[1] < sensor.y + HIT_THRESHOLD
                ):
                    self.dragging = True
                    self.dragged_item = sensor
                    break

            for waypoint in self.waypointHandler.waypoint_list:
                if (
                    mouse_pos[0] > waypoint.x - HIT_THRESHOLD
                    and mouse_pos[0] < waypoint.x + HIT_THRESHOLD
                    and mouse_pos[1] > waypoint.y - HIT_THRESHOLD
                    and mouse_pos[1] < waypoint.y + HIT_THRESHOLD
                ):
                    self.dragging = True
                    self.dragged_item = waypoint
                    break

        if self.dragging:
            self.dragged_item.x = mouse_pos[0]
            self.dragged_item.y = mouse_pos[1]
            self.draw_simulation(
                self.sensorHandler.sensor_list, self.waypointHandler.waypoint_list
            )
            if isinstance(self.dragged_item, Waypoint):
                self.dragged_item.update_reachable_sensors(self.sensorHandler.sensor_list)

            if isinstance(self.dragged_item, Sensor):
                for waypoint in self.waypointHandler.waypoint_list:
                    
                        waypoint.update_reachable_sensors(self.sensorHandler.sensor_list)

    def mouse_release_handler(self, sender):
        if self.dragging:
            self.dragging = False
            self.dragged_item = None
