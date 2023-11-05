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
        self.isGraphics = True

        width, height, channels, data = dpg.load_image("textures/sensor.png")

        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag="sensor")

        width, height, channels, data = dpg.load_image("textures/waypoint.png")

        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag="waypoint")

        width, height, channels, data = dpg.load_image("textures/grass.png")

        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag="grass")

        width, height, channels, data = dpg.load_image("textures/drone.png")

        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag="drone")

        width, height, channels, data = dpg.load_image("textures/depo.png")

        with dpg.texture_registry():
            dpg.add_static_texture(width, height, data, tag="depo")

        self.draw_map()

    def draw_map(self):
        if not self.isGraphics:
            tile_size = 25

            num_tiles_x = 1550 // tile_size
            num_tiles_y = 1050 // tile_size

            for i in range(num_tiles_x):
                for j in range(num_tiles_y):
                    dpg.draw_rectangle(
                        pmin=(i * tile_size, j * tile_size),
                        pmax=((i + 1) * tile_size, (j + 1) * tile_size),
                        color=(0, 150, 0, 255),
                        fill=(0, 150, 0, 255),
                        parent=self.drawlist,
                    )
                    # draw outline
                    dpg.draw_rectangle(
                        pmin=(i * tile_size, j * tile_size),
                        pmax=((i + 1) * tile_size, (j + 1) * tile_size),
                        color=(0, 0, 0, 255),
                        fill=(0, 0, 0, 0),
                        thickness=1,
                        parent=self.drawlist,
                    )

        else:
            image_size = 150

            num_images_x = (1550) // image_size
            num_images_y = (1050) // image_size

            for i in range(num_images_x):
                for j in range(num_images_y):
                    dpg.draw_image(
                        pmin=(i * image_size, j * image_size),
                        pmax=(
                            (i + 1) * image_size + 1,
                            (j + 1) * image_size + 1,
                        ),  # Increase the size of the images by 1 pixel
                        parent=self.drawlist,
                        texture_tag="grass",
                    )

    def draw_depo(self):
        if not self.isGraphics:
            dpg.draw_circle(
                center=(1550 / 2, 1050 / 2),
                radius=10,
                color=(0, 0, 0, 255),
                fill=(0, 0, 0, 255),
                parent=self.drawlist,
            )

        else:
            image_size = 100
            dpg.draw_image(
                pmin=(1550 / 2 - image_size / 2, 1050 / 2 - image_size / 2),
                pmax=(1550 / 2 + image_size / 2, 1050 / 2 + image_size / 2),
                parent=self.drawlist,
                texture_tag="depo",
            )

    def draw_sensors(self, sensor_list):
        # Remove all existing graphics if sensor_list is empty
        if len(sensor_list) == 0:
            self.remove_graphics(self.sensor_graphics)
            self.sensor_graphics = []
            return

        # Initialize graphics list if it doesn't exist
        if not hasattr(self, "sensor_graphics"):
            self.sensor_graphics = []

        # Draw new sensors
        for sensor in sensor_list[len(self.sensor_graphics) :]:
            graphic_id = self.draw_sensor(sensor)
            self.sensor_graphics.append(graphic_id)

        # Update existing sensors
        for sensor, graphic_id in zip(sensor_list, self.sensor_graphics):
            self.update_sensor(sensor, graphic_id)

    def draw_sensor(self, sensor):
        if self.isGraphics:
            image_size = 50
            return dpg.draw_image(
                pmin=(
                    sensor.x + 1550 / 2 - image_size / 2,
                    sensor.y + 1050 / 2 - image_size / 2,
                ),
                pmax=(
                    sensor.x + 1550 / 2 + image_size / 2,
                    sensor.y + 1050 / 2 + image_size / 2,
                ),
                parent=self.drawlist,
                texture_tag="sensor",
            )
        else:
            return dpg.draw_circle(
                center=(sensor.x + 1550 / 2, sensor.y + 1050 / 2),
                radius=10,
                color=(255, 255, 255, 255),
                fill=(255, 255, 255, 255),
                parent=self.drawlist,
            )

    def update_sensor(self, sensor, graphic_id):
        if self.isGraphics:
            image_size = 50
            dpg.configure_item(
                graphic_id,
                pmin=(
                    sensor.x + 1550 / 2 - image_size / 2,
                    sensor.y + 1050 / 2 - image_size / 2,
                ),
                pmax=(
                    sensor.x + 1550 / 2 + image_size / 2,
                    sensor.y + 1050 / 2 + image_size / 2,
                ),
            )
        else:
            dpg.configure_item(
                graphic_id,
                center=(sensor.x + 1550 / 2, sensor.y + 1050 / 2),
            )

    def draw_waypoints(self, waypoint_list):
        # Remove all existing graphics if waypoint_list is empty
        if len(waypoint_list) == 0:
            self.remove_graphics(self.waypoint_graphics)
            self.remove_graphics(self.waypoint_graphics_circle)
            self.waypoint_graphics = []
            self.waypoint_graphics_circle = []
            return

        # Initialize graphics lists if they don't exist
        if not hasattr(self, "waypoint_graphics"):
            self.waypoint_graphics = []
            self.waypoint_graphics_circle = []

        # Draw new waypoints
        for waypoint in waypoint_list[len(self.waypoint_graphics) :]:
            graphic_id = self.draw_waypoint(waypoint)
            dashed_circle_id = self.draw_dashed_circle(waypoint)
            self.waypoint_graphics.append(graphic_id)
            self.waypoint_graphics_circle.append(dashed_circle_id)

        # Update existing waypoints
        for waypoint, graphic_id, dashed_circle_id in zip(
            waypoint_list, self.waypoint_graphics, self.waypoint_graphics_circle
        ):
            self.update_waypoint(waypoint, graphic_id)
            self.update_dashed_circle(waypoint, dashed_circle_id)

    def remove_graphics(self, graphics_list):
        for graphic_id in graphics_list:
            dpg.delete_item(graphic_id)

    def draw_waypoint(self, waypoint):
        if self.isGraphics:
            image_size = 50
            return dpg.draw_image(
                pmin=(
                    waypoint.x + 1550 / 2 - image_size / 2,
                    waypoint.y + 1050 / 2 - image_size / 2,
                ),
                pmax=(
                    waypoint.x + 1550 / 2 + image_size / 2,
                    waypoint.y + 1050 / 2 + image_size / 2,
                ),
                parent=self.drawlist,
                texture_tag="waypoint",
            )
        else:
            return dpg.draw_circle(
                center=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
                radius=10,
                color=(255, 255, 0, 255),
                fill=(255, 255, 0, 255),
                parent=self.drawlist,
            )

    def draw_dashed_circle(self, waypoint):
        return dpg.draw_circle(
            center=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
            radius=100,
            color=(0, 0, 255, 255),
            parent=self.drawlist,
        )

    def update_waypoint(self, waypoint, graphic_id):
        if self.isGraphics:
            image_size = 50
            dpg.configure_item(
                graphic_id,
                pmin=(
                    waypoint.x + 1550 / 2 - image_size / 2,
                    waypoint.y + 1050 / 2 - image_size / 2,
                ),
                pmax=(
                    waypoint.x + 1550 / 2 + image_size / 2,
                    waypoint.y + 1050 / 2 + image_size / 2,
                ),
            )
        else:
            dpg.configure_item(
                graphic_id,
                center=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
            )

    def update_dashed_circle(self, waypoint, dashed_circle_id):
        dpg.configure_item(
            dashed_circle_id,
            center=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
        )

    def animate_drone_path(self, drone, waypoints):
        for waypoint in waypoints:
            steps: int = int(
                max((abs(drone.x - waypoint.x)), abs(drone.y - waypoint.y))
            )

            if steps == 0:
                continue

            # Calculate the amount to move in each step using integer division
            dx = (waypoint.x - drone.x) / steps
            dy = (waypoint.y - drone.y) / steps

            if not self.isGraphics:
                drone_id = dpg.draw_circle(
                    parent=self.drawlist,
                    center=(drone.x + 1550 / 2, drone.y + 1050 / 2),
                    radius=10,
                    color=(0, 0, 255, 255),
                    fill=(0, 0, 255, 255),
                )

            else:
                drone_id = dpg.draw_image(
                    pmin=(drone.x + 1550 / 2 - 50 / 2, drone.y + 1050 / 2 - 50 / 2),
                    pmax=(drone.x + 1550 / 2 + 50 / 2, drone.y + 1050 / 2 + 50 / 2),
                    parent=self.drawlist,
                    texture_tag="drone",
                )

            arrow_id = dpg.draw_arrow(
                parent=self.drawlist,
                p2=(drone.x + 1550 / 2, drone.y + 1050 / 2),
                p1=(waypoint.x + 1550 / 2, waypoint.y + 1050 / 2),
                thickness=2,
                color=(255, 255, 255, 255),
            )

            for _ in range(steps):
                # Update the drone's position and round the new position
                drone.x = drone.x + dx
                drone.y = drone.y + dy

                if not self.isGraphics:
                    dpg.configure_item(
                        drone_id,
                        center=(drone.x + 1550 / 2, drone.y + 1050 / 2),
                    )

                else:
                    dpg.configure_item(
                        drone_id,
                        pmin=(drone.x + 1550 / 2 - 50 / 2, drone.y + 1050 / 2 - 50 / 2),
                        pmax=(drone.x + 1550 / 2 + 50 / 2, drone.y + 1050 / 2 + 50 / 2),
                    )

                dpg.configure_item(
                    arrow_id,
                    p2=(drone.x + 1550 / 2, drone.y + 1050 / 2),
                )

                # Pause for a short time to create the animation effect
                time.sleep(0.01)

            # Wait the hovering time
            # time.sleep(waypoint.hovering_cost)

            # Remove the drone and arrow
            dpg.delete_item(drone_id)

            # change back waypoint color to yellow

    def draw_simulation(self, sensor_list, waypoint_list):
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
                self.dragged_item.update_reachable_sensors(
                    self.sensorHandler.sensor_list
                )
                self.waypointHandler.refresh_waypoint_combo()

            if isinstance(self.dragged_item, Sensor):
                self.sensorHandler.refresh_sensor_combo()
                for waypoint in self.waypointHandler.waypoint_list:
                    waypoint.update_reachable_sensors(self.sensorHandler.sensor_list)
                    self.waypointHandler.refresh_waypoint_combo()

    def mouse_release_handler(self, sender):
        if self.dragging:
            self.dragging = False
            self.dragged_item = None
