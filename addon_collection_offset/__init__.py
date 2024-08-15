bl_info = {
    "name": "Collection Offset Test",
    "blender": (4, 00, 0),
    "category": "Object",
}

import bpy
from mathutils import Matrix


def apply_location_offset(obj, collection_offset, inverse=False):
    """
    Adjusts the location of an object based on the collection's offset.
    When inverse is False, moves the object so that its distance from the world origin matches its distance from the collection offset.
    When inverse is True, moves the object back to its original position relative to the collection offset.
    """
    if inverse:
        offset_matrix = Matrix.Translation(collection_offset)
    else:
        offset_matrix = Matrix.Translation(-collection_offset)

    # Decompose the matrix_world into translation, rotation, and scale
    loc, rot, scale = obj.matrix_world.decompose()

    # Rebuild the matrix_world with the applied offset
    # We only modify the location component here
    new_loc = offset_matrix @ Matrix.Translation(loc)

    # Construct the final transformation matrix using the unchanged rotation and scale
    obj.matrix_world = new_loc @ rot.to_matrix().to_4x4() @ Matrix.Diagonal(scale).to_4x4()


def apply_collection_offset(collection, inverse=False):
    """
    Applies or removes the collection's instance offset to all objects in the collection,
    moving them relative to the world origin.
    """
    collection_offset = collection.instance_offset

    for obj in collection.all_objects:
        if obj.parent is None:  # Only apply to top-level objects
            apply_location_offset(obj, collection_offset, inverse)


class OBJECT_OT_ApplyOffset(bpy.types.Operator):
    bl_idname = "object.apply_offset"
    bl_label = "Apply Offset"
    bl_options = {'REGISTER', 'UNDO'}

    collection_name: bpy.props.StringProperty()

    def execute(self, context):
        collection = bpy.data.collections.get(self.collection_name)
        if not collection:
            self.report({'ERROR'}, f"Collection '{self.collection_name}' not found.")
            return {'CANCELLED'}

        apply_collection_offset(collection, inverse=False)
        self.report({'INFO'}, f"Offset applied to collection '{self.collection_name}'.")
        return {'FINISHED'}


class OBJECT_OT_InverseOffset(bpy.types.Operator):
    bl_idname = "object.inverse_offset"
    bl_label = "Inverse Offset"
    bl_options = {'REGISTER', 'UNDO'}

    collection_name: bpy.props.StringProperty()

    def execute(self, context):
        collection = bpy.data.collections.get(self.collection_name)
        if not collection:
            self.report({'ERROR'}, f"Collection '{self.collection_name}' not found.")
            return {'CANCELLED'}

        apply_collection_offset(collection, inverse=True)
        self.report({'INFO'}, f"Inverse offset applied to collection '{self.collection_name}'.")
        return {'FINISHED'}


def draw_collection_buttons(self, context):
    layout = self.layout
    collection = context.collection

    row = layout.row(align=True)
    op = row.operator("object.apply_offset", text="Apply Offset")
    op.collection_name = collection.name

    op = row.operator("object.inverse_offset", text="Inverse Offset")
    op.collection_name = collection.name


def register():
    bpy.utils.register_class(OBJECT_OT_ApplyOffset)
    bpy.utils.register_class(OBJECT_OT_InverseOffset)

    # Add the button to the COLLECTION_PT_instancing panel
    bpy.types.COLLECTION_PT_instancing.append(draw_collection_buttons)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ApplyOffset)
    bpy.utils.unregister_class(OBJECT_OT_InverseOffset)

    # Remove the button from the COLLECTION_PT_instancing panel
    bpy.types.COLLECTION_PT_instancing.remove(draw_collection_buttons)


if __name__ == "__main__":
    register()
