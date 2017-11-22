bl_info = {
    "name": "New Object",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

def alignObjects(new, old):
    new.matrix_world = old.matrix_world

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


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        activeObject = bpy.context.object

        vertices = getBoundingBox(self,context)
        newObj = add_object(self, context, vertices)
        print ("LOOOL")
        alignObjects(newObj, activeObject)
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
