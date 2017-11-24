import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from .assets import colliderEnum, ColliderAsset

from .func import *

def renameCollider(self,context,colliderOb):
    allObjects = bpy.data.objects
    prefix =self.my_string + "_"
    print ("MY STRING " + prefix)

    for i, obj in enumerate(colliderOb):
        z = 0
        parName = obj.parent.name
        endNumeration = ('%02d' % (i + z))
        newName =  prefix + parName + "_" + endNumeration

        while (newName in allObjects):
            endNumeration = ('%02d' % (i + z))
            newName = prefix + parName + "_" + endNumeration
            z += 1

        obj.name = newName
        obj.draw_type = 'WIRE'


class OBJECT_OT_addCollider(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_collider"
    bl_label = "Add BBox Collider"
    bl_options = {'REGISTER', 'UNDO'}

    my_convert = bpy.props.BoolProperty(name="Replace Old", default=False)
    my_float = bpy.props.FloatProperty(name="InflateColission",  default= -0.5)
    my_string = bpy.props.EnumProperty(
        items=colliderEnum.items,
        name="Collision Type",
        default = 'UBX',
        description="",
        )
    #my_replace = bpy.props.StringProperty(name="Colission Post", default = "_edit")
    my_deleteBevel = bpy.props.BoolProperty(name="Delete Bevel", default=False)
    my_deleteSubsurf = bpy.props.BoolProperty(name="Delete Subsurf", default=True)

    @classmethod
    def poll(cls, context):
        for obj in bpy.context.selected_objects:
            if obj.parent is None:
                return False
        if context.active_object is None:
            return False
        return True


    def execute(self, context):
        activeObject = bpy.context.object
        selectedObjects = bpy.context.selected_objects.copy()
        colliderOb = []


        for i, obj in enumerate(selectedObjects):
            if self.my_convert == False:
                bBox = getBoundingBox(self,context,obj)         # create BoundingBox object for collider
                newCollider = add_object(self, context, bBox, obj.name + "_collider")
                alignObjects(newCollider, obj)
                newCollider.parent = obj.parent  # parent object oriented
                newCollider.matrix_local = obj.matrix_local
            else:
                newCollider = obj
                for mod in obj.modifiers:
                    if mod.type == 'BEVEL':
                        if self.my_deleteBevel == True:
                            obj.modifiers.remove(mod)
                        else:
                            mod.segments = 1

                    elif mod.type == 'SUBSURF':
                        if self.my_deleteSubsurf == True:
                            obj.modifiers.remove(mod)
                        else:
                            mod.levels = 1

            mod = newCollider.modifiers.new(name="ColliderOffset_disp", type='DISPLACE')
            mod.strength = self.my_float

            asset = ColliderAsset(obj.name).getDictionary()
            print('ASSET' + str(asset))
            newCollider['asset'] = asset
            newCollider.asset_type = 'asset_collider'

            colliderOb.append(newCollider)

        renameCollider(self, context,colliderOb)

        for col in colliderOb:
            col.select = True

        return {'FINISHED'}



def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Object",
        icon='PLUGIN')


# This allows you to right click on a button and link to the manual
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/dev/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "editors/3dview/object"),
        )
    return url_manual_prefix, url_manual_mapping



if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


