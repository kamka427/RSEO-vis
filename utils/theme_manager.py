import dearpygui.dearpygui as dpg
import dearpygui_ext.themes as themes


class ThemeManager:
    def __init__(self):
        self.light_theme = themes.create_theme_imgui_light()
        self.dark_theme = themes.create_theme_imgui_dark()

        with dpg.window(label="Theme Selector", width=200, height=100, pos=(10, 10)):
            dpg.add_combo(
                ["Light", "Dark"],
                label="Theme",
                callback=self.set_theme,
                default_value="Dark",
            )

    def set_theme(self, sender, data):
        if dpg.get_value(sender) == "Light":
            dpg.bind_theme(self.light_theme)
        else:
            dpg.bind_theme(self.dark_theme)
