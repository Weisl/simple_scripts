import bpy
import os

bl_info = {
    "name": "Custom Save",
    "description": "Master Custom Save",
    "author": "Matthias Patscheider",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "View3D",
    "warning": "This is an unstable version",
    "wiki_url": "",
    "category": "Object"}


class ExportPreferences(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__  ### __package__ works on multifile and __name__ not

    filepath = StringProperty(
        name="Project File Path",
        subtype='FILE_PATH',
    )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Save Settings")
        box.prop(self, "filepath")


class SaveOperator(bpy.types.Operator):
    bl_idname = "project.save_op"
    bl_label = "Save scene"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}


class PopupTest(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "popup.exportinfo"
    bl_label = "Export Panel: " + "0, 5, 0  Beta"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        width = 800 * bpy.context.user_preferences.system.pixel_size
        status = context.window_manager.invoke_props_dialog(self, width=width)

        return status

    def draw(self, context):
        wm = bpy.context.window_manager
        layout = self.layout

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences

        box = layout.box()

    def execute(self, context):
        ob = context.object
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
