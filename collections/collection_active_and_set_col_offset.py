"""Create collection from object and sett instance offset based on the object. """

import bpy

activeOb = bpy.context.view_layer.objects.active

for ob in bpy.context.selected_objects:

    collection_name = ob.name + "_col"

    if collection_name not in bpy.data.collections:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)

    collection = bpy.data.collections[collection_name]
    collection.objects.link(ob)

    collection.instance_offset[0] = ob.location.x
    collection.instance_offset[1] = ob.location.y
    collection.instance_offset[2] = ob.location.z
