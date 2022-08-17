"""move selected object to zero"""
import bpy
for obj in bpy.context.selectable_objects:
    bpy.context.view_layer.objects.active = obj
    
    bpy.context.object.location[0] = 0
    bpy.context.object.location[1] = 0
    bpy.context.object.location[2] = 0

    