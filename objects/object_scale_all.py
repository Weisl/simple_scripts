"""scale all selected objects"""
import bpy

scaleVactor = 1;

for obj in bpy.context.selected_objects:
    bpy.context.view_layer.objects.active = obj
    
    bpy.context.object.scale[0] = scaleVactor
    bpy.context.object.scale[1] = scaleVactor
    bpy.context.object.scale[2] = scaleVactor