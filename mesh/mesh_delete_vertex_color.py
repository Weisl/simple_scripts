""" Delete all vertex color channels of the selected objects. """

import bpy

for ob in bpy.context.selected_objects:
    if ob.type == "MESH":
        for vrC in ob.data.vertex_colors:
            ob.data.vertex_colors.remove(vrC)
