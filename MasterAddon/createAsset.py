import bpy

class AssetCreate(bpy.types.Operator):
    bl_idname = "master.asset_create"
    bl_label = "Create Asset"
    bl_description = "Create Asset"
    bl_options = {'REGISTER', 'UNDO'}

    my_parentSize = bpy.props.FloatProperty(name="Socket Size",  default= 15)

    @classmethod
    def poll(cls, context):
        if bpy.context.selected_objects == None:
            return False
        return True

    def execute(self, context):
        selection = bpy.context.selected_objects.copy()
        assetList = main(self, selection)
        return {"FINISHED"}


def main(self, selection):

    for obj in selection:

        wMatrix = obj.matrix_world

        emptyName = "SM_" + obj.name

        empty = bpy.data.objects.new("empty", None)
        bpy.context.scene.objects.link(empty)
        empty.empty_draw_size = self.my_parentSize
        empty.empty_draw_type = 'CUBE'
        empty.name = emptyName
        empty.select = True

        empty.matrix_world = wMatrix
        obj.parent = empty

        obj.matrix_local = ((1.0, 0.0, 0.0, 0.0),
                (0.0, 1.0, 0.0, 0.0),
                (0.0, 0.0, 1.0, 0.0),
                (0.0, 0.0, 0.0, 1.0))
