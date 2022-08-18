"""Assign uniform scale to all selected objects. Change the output scale with the 'caleFactor' variable"""
import bpy

scaleFactor = 1

for obj in bpy.context.selected_objects:
    bpy.context.view_layer.objects.active = obj

    bpy.context.object.scale[0] = scaleFactor
    bpy.context.object.scale[1] = scaleFactor
    bpy.context.object.scale[2] = scaleFactor
