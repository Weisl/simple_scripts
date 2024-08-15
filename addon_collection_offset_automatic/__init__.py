import bpy

bl_info = {
    "name": "Collection Offset by Object",
    "blender": (4, 0, 0),
    "category": "Object",
}


def set_collection_offset_from_object(collection, obj):
    """Set the collection offset to the object's location."""
    if collection and obj:
        collection.instance_offset = obj.location


def update_collection_offset(scene):
    """Update the collection offset when the object is moved."""
    for collection in bpy.data.collections:
        obj = collection.get("offset_object", None)
        if obj:
            if collection.instance_offset != obj.location:
                set_collection_offset_from_object(collection, obj)


class COLLECTION_PT_instancing_offset(bpy.types.Panel):
    """Extend the Instancing Panel in the Collection properties window"""
    bl_label = "Instancing"
    bl_idname = "COLLECTION_PT_instancing_offset"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"
    bl_parent_id = "COLLECTION_PT_instancing"

    def draw(self, context):
        layout = self.layout
        collection = context.collection

        # Draw existing instancing properties
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        layout.prop(collection, "instance_offset")

        # Add the Object Picker
        layout.prop(collection, "offset_object", text="Offset Object")

        # Add an operator button to manually update the offset if needed
        layout.operator("object.set_collection_offset", text="Set Collection Offset")


class OBJECT_OT_set_collection_offset(bpy.types.Operator):
    """Set the collection offset to the selected object's location."""
    bl_idname = "object.set_collection_offset"
    bl_label = "Set Collection Offset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        collection = context.collection
        obj = collection.offset_object
        if not obj:
            self.report({'WARNING'}, "No object selected")
            return {'CANCELLED'}

        # Set the collection offset
        set_collection_offset_from_object(collection, obj)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_set_collection_offset)
    bpy.utils.register_class(COLLECTION_PT_instancing_offset)

    bpy.types.Collection.offset_object = bpy.props.PointerProperty(
        name="Offset Object",
        type=bpy.types.Object,
        description="Object to be used for setting the collection offset"
    )

    if update_collection_offset not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(update_collection_offset)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_set_collection_offset)
    bpy.utils.unregister_class(COLLECTION_PT_instancing_offset)

    del bpy.types.Collection.offset_object

    if update_collection_offset in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(update_collection_offset)


if __name__ == "__main__":
    register()
