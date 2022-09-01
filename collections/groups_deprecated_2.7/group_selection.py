"""add selected objects to group"""
import bpy

groupname = "wall_panelling_HP"


def setActive(obj):
    bpy.context.view_layer.objects.active = obj


for obj in bpy.context.selected_objects:
    setActive(obj)
    bpy.ops.object.group_link(group=groupname)
