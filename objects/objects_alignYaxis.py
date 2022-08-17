""" align objects in y axis"""

import bpy

selected = bpy.context.selected_objects
i = 0
dist = 0
for obj in selected:
    obj.location.z = 0
    obj.location.x = 0

    if i == 0:
        obj.location.y = 0
        dist += obj.dimensions.y / 2
    else:
        obj.location.y = dist + obj.dimensions.y / 2
        dist += obj.dimensions.y
    i += 1
