import bpy

bl_info = {
    "name": "New Collider",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }






from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add

def alignObjects(new, old):
    new.matrix_world = old.matrix_world

def applyMod(obj):
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')

    if obj is not None:
        for modi in obj.modifiers:
            try:
                midifiername = modi.name
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=midifiername)
            except (RuntimeError):
                obj.modifiers.remove(modi)


def add_object(self, context, vertices):

    verts = vertices
    edges = []
    faces = [[0, 1, 2, 3],[7,6,5,4],[5,6,2,1],[4,7,3,0],[3,2,6,7],[4,5,1,0]]

    mesh = bpy.data.meshes.new(name="Collider")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    newObj = object_data_add(context, mesh, operator=self) # links to object instance
    return newObj.object

def getBoundingBox(self,context):
    return context.object.bound_box

def duplicateObject(ob):
    me = ob.data # use current object's data
    me_copy = me.copy()
    me_copy.name = me.name + "_copy"

    new_ob = bpy.data.objects.new(ob.name + "_clone", me_copy)

    new_ob.matrix_world  = ob.matrix_world

    scene = bpy.context.scene
    scene.objects.link(new_ob)
    scene.update()

    new_ob.select = True
    bpy.context.scene.objects.active = ob
    bpy.ops.object.make_links_data(type='MODIFIERS')
    bpy.ops.object.make_links_data(type='MATERIAL')
    return new_ob

def main(self,context, selectedObjects, colliderOb):
    allObjects = bpy.data.objects

    for obj in selectedObjects:
        parName = obj.parent.name
        collider = colliderOb
        #collider = duplicateObject(obj)

        for mod in collider.modifiers:
            if mod.type == 'BEVEL' and self.my_bool == True:
                collider.modifiers.remove(mod)
            elif mod.type == 'SUBSURF' and self.my_bool2 == True:
                collider.modifiers.remove(mod)


        i = 1
        endNumeration = ('%02d' % i)
        newName = self.my_string + parName + "_" + endNumeration
        while (newName in allObjects):
            endNumeration = ('%02d' % i)
            newName = self.my_string + parName + "_" + endNumeration
            i = i + 1

        applyMod(collider)
        collider.name = newName
        collider.draw_type = 'WIRE'

        collider.select = True

        bpy.context.scene.objects.active = obj.parent
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)





class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    my_float = bpy.props.FloatProperty(name="InflateColission",  default= -0.5)
    my_bool = bpy.props.BoolProperty(name="Remove Bevel", default = True)
    my_bool2 = bpy.props.BoolProperty(name="Remove Subdivision Surface", default = True)
    my_string = bpy.props.StringProperty(name="Colission Prefix", default = "UCX_")


    @classmethod
    def poll(cls, context):
        if context.active_object is not None and context.active_object.parent is not None:
            return True
        else: # no object is active or object has no parent:
            return False

    def execute(self, context):
        activeObject = bpy.context.object
        selectedObjects = bpy.context.selected_objects.copy()

        vertices = getBoundingBox(self,context)
        colliderOb = add_object(self, context, vertices)
        main(self, context,selectedObjects,colliderOb)
        alignObjects(colliderOb, activeObject)
        return {'FINISHED'}


# Registration

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


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
