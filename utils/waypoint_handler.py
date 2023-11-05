import dearpygui.dearpygui as dpg
from objects.waypoint import Waypoint


class WaypointHandler:
    def __init__(self, waypoint_list):
        self.waypoint_list = waypoint_list

    def create_waypoint(self, sender, data):
        x_cord_w = dpg.get_value(self.x_cord_w_c)
        y_cord_w = dpg.get_value(self.y_cord_w_c)
        radius = dpg.get_value(self.radius_c)
        flying_cost = dpg.get_value(self.flying_cost_c)
        hovering_cost = dpg.get_value(self.hovering_cost_c)

        waypoint = Waypoint(
            "w1", x_cord_w, y_cord_w, [], flying_cost, radius, hovering_cost
        )
        self.waypoint_list.append(waypoint)
        print(f"Waypoint {waypoint} added")

        dpg.configure_item(item=self.waypoint_combo, items=self.waypoint_list)

        self.redraw_simulation()
        return self.waypoint_list

    def delete_waypoint(self, sender, data):
        selected_waypoint_str = dpg.get_value(item=self.waypoint_combo)
        for waypoint in self.waypoint_list:
            if str(waypoint) == selected_waypoint_str:
                selected_waypoint = waypoint
                break
        else:
            print("No waypoint selected")
            return

        self.waypoint_list.remove(selected_waypoint)
        print(f"Waypoint {selected_waypoint} removed")

        dpg.configure_item(item=self.waypoint_combo, items=self.waypoint_list)
        dpg.set_value(item=self.waypoint_combo, value="")

        self.redraw_simulation()
        return self.waypoint_list

    def set_redraw_simulation(self, redraw_simulation):
        self.redraw_simulation = redraw_simulation

    def create_add_waypoint_window(self, width, height, pos):
        with dpg.window(label="Add Waypoint", width=width, height=height, pos=pos):
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

    def create_waypoint_list_window(self, width, height, pos):
        with dpg.window(label="Waypoint List", width=width, height=height, pos=pos):
            self.waypoint_combo = dpg.add_combo(
                label="Waypoint", items=self.waypoint_list
            )
            dpg.add_button(label="Delete Waypoint", callback=self.delete_waypoint)
