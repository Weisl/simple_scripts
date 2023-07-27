'''
Convert Face Corner Attributes to UV maps. Useful for Geometry Nodes.
based on: https://blender.stackexchange.com/questions/250867/overwrite-original-geometry-uvmap-with-geometry-nodes-uv-map'''

import bpy

UVAttributeName = 'customUV'
for obj in bpy.context.selected_objects.copy():
    bpy.context.view_layer.objects.active = obj
    a = bpy.context.object.data.attributes
    a.active = a[UVAttributeName]
    bpy.ops.geometry.attribute_convert(mode='GENERIC', domain='CORNER', data_type='FLOAT2')