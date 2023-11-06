import dearpygui.dearpygui as dpg
from objects.drone import Drone


class DroneHandler:
    def __init__(self, drone_list):
        self.drone_list = drone_list

    def create_drone(self, sender, data):
        energy = dpg.get_value(self.energy_c)
        storage = dpg.get_value(self.storage_c)
        drone = Drone(energy, storage)
        self.drone_list.append(drone)
        print(f"Drone {drone} added")

        dpg.configure_item(item=self.drone_combo, items=self.drone_list)

        return self.drone_list

    def delete_drone(self, sender, data):
        selected_drone_str = dpg.get_value(item=self.drone_combo)
        for drone in self.drone_list:
            if str(drone) == selected_drone_str:
                selected_drone = drone
                break
        else:
            print("No drone selected")
            return

        self.drone_list.remove(selected_drone)
        print(f"Drone {selected_drone} removed")

        dpg.configure_item(item=self.drone_combo, items=self.drone_list)
        dpg.set_value(item=self.drone_combo, value="")

        return self.drone_list

    def create_add_drone_window(self, width, height, pos):
        with dpg.window(label="Add Drone", width=width, height=height, pos=pos):
            self.energy_c = dpg.add_input_int(label="Energy", default_value=100)
            self.storage_c = dpg.add_input_int(label="Storage", default_value=10)
            dpg.add_button(label="Add Drone", callback=self.create_drone)

    def create_drone_list_window(self, width, height, pos):
        with dpg.window(label="Drone List", width=width, height=height, pos=pos):
            self.drone_combo = dpg.add_combo(label="Drone", items=self.drone_list)
            dpg.add_button(label="Delete Drone", callback=self.delete_drone)
