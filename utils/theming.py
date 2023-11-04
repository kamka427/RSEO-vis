import dearpygui.dearpygui as dpg
import dearpygui_ext.themes as themes

light_theme = themes.create_theme_imgui_light()
dark_theme = themes.create_theme_imgui_dark()


def set_theme(sender, data):
    if dpg.get_value(sender) == "Light":
        dpg.bind_theme(light_theme)
    else:
        dpg.bind_theme(dark_theme)


def create_theme_selector():
    with dpg.window(label="Theme Selector", width=200, height=100, pos=(10, 10)):
        dpg.add_combo(
            ["Light", "Dark"], label="Theme", callback=set_theme, default_value="Dark"
        )
