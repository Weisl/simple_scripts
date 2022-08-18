"""Select all objects that have a uniform scale of 1.0"""
import bpy

selected = bpy.context.selected_objects.copy()
new_selection = []

for obj in selected:
    if obj.scale[0] == 1.0 and obj.scale[1] == 1.0 and obj.scale[2] == 1.0:
        new_selection.append(obj)

bpy.ops.object.select_all(action='DESELECT')

for ob in new_selection:
    ob.select_set(True)
