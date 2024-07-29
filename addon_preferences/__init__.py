import bpy
from bpy.types import Operator, AddonPreferences, Menu
from bpy.props import StringProperty
from bl_operators.presets import AddPresetBase

bl_info = {
    "name": "Preferences Preset Add-On",
    "description": "An add-on with preferences that include two string properties and a preset system.",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Preferences",
    "warning": "",
    "wiki_url": "",
    "category": "Preferences"
}

# Set ADDON_NAME based on __package__, with a fallback for direct script execution
ADDON_NAME = __package__ if __package__ else "preferences_preset_addon"
folder_name = 'preferences_presets'


class SimplePreferences(AddonPreferences):
    bl_idname = ADDON_NAME

    string_a: StringProperty(
        name="String A",
        description="First string parameter",
        default="Default A"
    )

    string_b: StringProperty(
        name="String B",
        description="Second string parameter",
        default="Default B"
    )

    def draw(self, context):
        layout = self.layout
        panel_func(self, context)  # Call panel_func to prepend the preset menu and buttons

        layout.prop(self, "string_a")
        layout.prop(self, "string_b")


class PREFS_MT_prefs_preset(Menu):
    bl_label = "Preferences Presets"
    preset_subdir = folder_name
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


class ADD_OT_PresetRenamingPresets(AddPresetBase, Operator):
    """Add a preference preset"""
    bl_idname = 'preferences.add_preset'
    bl_label = 'Add Preference Preset'
    preset_menu = 'PREFS_MT_prefs_preset'

    # Common variable used for all preset values
    preset_defines = [
        f'prefs = bpy.context.preferences.addons["{ADDON_NAME}"].preferences'
    ]

    # Properties to store in the preset
    preset_values = [
        'prefs.string_a',
        'prefs.string_b',
    ]

    # Directory to store the presets
    preset_subdir = folder_name


def panel_func(self, context):
    layout = self.layout

    row = layout.row(align=True)
    row.menu('PREFS_MT_prefs_preset', text=PREFS_MT_prefs_preset.bl_label)
    row.operator(ADD_OT_PresetRenamingPresets.bl_idname, text="", icon='ADD')
    row.operator(ADD_OT_PresetRenamingPresets.bl_idname, text="", icon='REMOVE').remove_active = True


classes = (
    SimplePreferences,
    PREFS_MT_prefs_preset,
    ADD_OT_PresetRenamingPresets,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
