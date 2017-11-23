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
        row.label("Quick")
        row = layout.row()
        row.operator("master.conver_apply_merge")


        row = layout.row()
        row.label("Asset manager")
        row.label("Todo Convert to asst")
        row.label("Create new Asset")


        row = layout.row()
        row.label("Collider")

        row = layout.row()
        row.operator("mesh.add_collider", text = "Collider From BBox").my_convert = False
        row = layout.row()
        row.operator("mesh.add_collider", text = "Convert To Collider").my_convert = True

        # Create an row where the buttons are aligned to each other.
        # layout.label(text=" Aligned Row:")

        #row = layout.row(align=True)
        #row.prop(scene, "frame_start")
        #row.prop(scene, "frame_end")

        # Create two columns, by using a split layout.
        #split = layout.split()

        # First column
        #col = split.column()
        #col.label(text="Column One:")
        #col.prop(scene, "frame_end")
        #col.prop(scene, "frame_start")

        # Second column, aligned
        #col = split.column(align=True)
        #col.label(text="Column Two:")
        #col.prop(scene, "frame_start")
        #col.prop(scene, "frame_end")
