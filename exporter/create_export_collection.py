import bpy

class OBJECT_OT_CreateCollectionWithChildren(bpy.types.Operator):
    """
    Create a new collection for the active object and its children.
    """
    bl_idname = "object.create_collection_with_children"
    bl_label = "Create Collection with Children"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_object = context.active_object
        parent_collection = context.scene.parent_collection

        if not active_object:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}

        # Create a new collection named after the active object
        new_collection = bpy.data.collections.new(active_object.name)

        # Add the new collection to the specified parent collection or the scene
        if parent_collection:
            parent_collection.children.link(new_collection)
        else:
            context.scene.collection.children.link(new_collection)

        # Link the active object and its children recursively to the new collection
        def link_object_and_all_children(collection, obj):
            collection.objects.link(obj)
            for child in obj.children:
                link_object_and_all_children(collection, child)

        link_object_and_all_children(new_collection, active_object)

        # Assign a collection exporter to the new collection
        self.assign_collection_exporter(new_collection)

        self.report({'INFO'}, f"Collection '{new_collection.name}' created and linked.")
        return {'FINISHED'}

    def assign_collection_exporter(self, collection, export_format):
        # Add a collection exporter for the specified format
        bpy.context.view_layer.objects.active = None  # Ensure no active object conflicts
        result = bpy.ops.collection.exporter_add(name=f"IO_FH_{export_format.lower()}")
        if result == {'FINISHED'}:
            for exporter in bpy.data.exporters:
                if exporter.collection is None:
                    exporter.collection = collection
                    break


class OBJECT_PT_CollectionToolPanel(bpy.types.Panel):
    bl_label = "Collection Tools"
    bl_idname = "OBJECT_PT_collection_tool_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Collections'

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "parent_collection", text="Parent Collection")
        layout.operator(OBJECT_OT_CreateCollectionWithChildren.bl_idname)


# Register scene properties and classes
def register():
    bpy.types.Scene.parent_collection = bpy.props.PointerProperty(
        name="Parent Collection",
        description="Choose the parent collection to link the new collection to",
        type=bpy.types.Collection
    )
    bpy.utils.register_class(OBJECT_OT_CreateCollectionWithChildren)
    bpy.utils.register_class(OBJECT_PT_CollectionToolPanel)


def unregister():
    del bpy.types.Scene.parent_collection
    bpy.utils.unregister_class(OBJECT_OT_CreateCollectionWithChildren)
    bpy.utils.unregister_class(OBJECT_PT_CollectionToolPanel)


if __name__ == "__main__":
    register()
