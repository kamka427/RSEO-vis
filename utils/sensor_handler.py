import dearpygui.dearpygui as dpg
from objects.sensor import Sensor


class SensorHandler:
    def __init__(self, sensor_list):
        self.sensor_list = sensor_list

    def create_sensor(self, sender, data):
        reward = dpg.get_value(self.reward_c)
        data_size = dpg.get_value(self.data_size_c)
        x_cord_s = dpg.get_value(self.x_cord_s_c)
        y_cord_s = dpg.get_value(self.y_cord_s_c)
        hovering_cost = dpg.get_value(self.hovering_cost_c)

        sensor = Sensor("p1", reward, data_size, x_cord_s, y_cord_s, hovering_cost)
        self.sensor_list.append(sensor)
        print(f"Sensor {sensor} added")

        dpg.configure_item(item=self.sensor_combo, items=self.sensor_list)

        self.redraw_simulation()
        return self.sensor_list

    def delete_sensor(self, sender, data):
        selected_sensor_str = dpg.get_value(item=self.sensor_combo)
        for sensor in self.sensor_list:
            if str(sensor) == selected_sensor_str:
                selected_sensor = sensor
                break
        else:
            print("No sensor selected")
            return

        self.sensor_list.remove(selected_sensor)
        print(f"Sensor {selected_sensor} removed")

        dpg.configure_item(item=self.sensor_combo, items=self.sensor_list)
        dpg.set_value(item=self.sensor_combo, value="")

        self.redraw_simulation()
        return self.sensor_list

    def set_redraw_simulation(self, redraw_simulation):
        self.redraw_simulation = redraw_simulation

    def create_add_sensor_window(self, width, height, pos):
        with dpg.window(label="Add Sensor", width=width, height=height, pos=pos):
            self.reward_c = dpg.add_input_int(label="Reward", default_value=100)
            self.data_size_c = dpg.add_input_int(label="Data Size", default_value=10)
            self.x_cord_s_c = dpg.add_input_int(label="X", default_value=100)
            self.y_cord_s_c = dpg.add_input_int(label="Y", default_value=100)
            self.hovering_cost_c = dpg.add_input_int(
                label="Hovering Cost", default_value=5
            )
            dpg.add_button(label="Add Sensor", callback=self.create_sensor)

    def create_sensor_list_window(self, width, height, pos):
        with dpg.window(label="Sensor List", width=width, height=height, pos=pos):
            self.sensor_combo = dpg.add_combo(label="Sensor", items=self.sensor_list)
            dpg.add_button(label="Delete Sensor", callback=self.delete_sensor)
