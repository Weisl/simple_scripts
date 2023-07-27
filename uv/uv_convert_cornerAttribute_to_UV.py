'''
Convert Face Corner Attributes to UV maps. Useful for Geometry Nodes.
based on: https://blender.stackexchange.com/questions/250867/overwrite-original-geometry-uvmap-with-geometry-nodes-uv-map'''

import bpy
selected_objects = bpy.context.selected_objects.copy()
active_object = bpy.context.active_object
for obj in selected_objects:
    for ob in selected_objects:
        ob.select_set(False)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.context.view_layer.objects.active = obj
    a = obj.data.attributes
    a.active = a['customUV']
    bpy.ops.geometry.attribute_convert(mode='GENERIC', domain='CORNER', data_type='FLOAT2')