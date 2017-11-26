import bpy

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Layout Demo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        wm = bpy.context.window_manager
        row.prop(wm, "csv_dir")




        row = layout.row()
        row.label("Change File Extensions")
        row = layout.row()
        row.operator("images.path_change_extension")
        row.operator("images.path_export_csv_old")
        row = layout.row()
        row.operator("images.path_export_csv", text = "New CSV").my_append = False
        row.operator("images.path_export_csv", text = "Append CSV").my_append = True
        row.operator("images.path_import_csv")
        row = layout.row()
        row.operator("images.find_in_csv")
        row.operator("images.load_from_csv")
        row.operator("images.load_from_csv_02")


