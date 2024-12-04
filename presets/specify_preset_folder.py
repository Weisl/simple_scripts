import bpy
import os


def get_presets_folder():
    """Retrieve the base path for Blender's presets folder."""
    # Get the user scripts folder dynamically
    return os.path.join(bpy.utils.resource_path('USER'), "scripts", "presets", "operator")


EXPORT_PRESET_FOLDERS = {
    "FBX": os.path.join(get_presets_folder(), "export_scene.fbx"),
    "OBJ": os.path.join(get_presets_folder(), "wm.obj_export"),
    "GLTF": os.path.join(get_presets_folder(), "export_scene.gltf"),
    "USD": os.path.join(get_presets_folder(), "wm.usd_export"),
    "ALEMBIC": os.path.join(get_presets_folder(), "wm.alembic_export"),
}


class SimpleExporterProperties(bpy.types.PropertyGroup):
    export_format: bpy.props.EnumProperty(
        name="Export Format",
        description="Select the export format",
        items=[
            ("FBX", "FBX", "FBX Export"),
            ("OBJ", "OBJ", "OBJ Export"),
            ("GLTF", "glTF", "glTF Export"),
            ("USD", "USD", "USD Export"),
            ("ALEMBIC", "Alembic", "Alembic Export"),
        ],
        default="FBX",
        update=lambda self, context: self.update_preset_path()
    )
    preset_path: bpy.props.StringProperty(
        name="Preset Folder Path",
        description="Path to the folder containing .py files",
        default="",
        subtype='DIR_PATH',
    )
    simple_exporter_preset_path: bpy.props.EnumProperty(
        name="Preset File",
        description="Select a .py file",
        items=lambda self, context: self.get_py_files(),
    )
    override_path: bpy.props.BoolProperty(
        name="Override Preset Folder",
        description="Manually override the automatically set preset folder",
        default=False,
    )

    def update_preset_path(self):
        """Automatically set the preset path based on the export format unless overridden."""
        if not self.override_path:
            self.preset_path = EXPORT_PRESET_FOLDERS.get(self.export_format, "")

    def get_py_files(self):
        """Retrieve all .py files from the specified folder."""
        if not self.preset_path:
            return [("", "No Path", "No path specified")]

        try:
            files = [
                (os.path.join(self.preset_path, f), f, "")
                for f in os.listdir(self.preset_path)
                if f.endswith(".py")
            ]
            return files if files else [("", "No Files", "No .py files found")]
        except Exception as e:
            return [("", "Error", str(e))]


class SimpleExporterPanel(bpy.types.Panel):
    bl_label = "Simple Exporter"
    bl_idname = "SCENE_PT_simple_exporter"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout
        props = context.scene.simple_exporter_props

        layout.prop(props, "export_format", text="Export Format")
        layout.prop(props, "override_path", text="Override Preset Folder")

        row = layout.row(align=True)
        row.enabled = props.override_path  # Only enable preset_path editing if override_path is true
        row.prop(props, "preset_path", text="Preset Folder")

        layout.prop(props, "simple_exporter_preset_path", text="Preset File")


def register():
    bpy.utils.register_class(SimpleExporterProperties)
    bpy.utils.register_class(SimpleExporterPanel)
    bpy.types.Scene.simple_exporter_props = bpy.props.PointerProperty(type=SimpleExporterProperties)


def unregister():
    bpy.utils.unregister_class(SimpleExporterProperties)
    bpy.utils.unregister_class(SimpleExporterPanel)
    del bpy.types.Scene.simple_exporter_props


if __name__ == "__main__":
    register()
