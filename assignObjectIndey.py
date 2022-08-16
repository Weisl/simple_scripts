'''Assigns a RenderID to the selected Objects '''

import bpy

renderIdIdx = 1

selected_objects = bpy.context.selected_objects.copy()
for obj in selected_objects:
    obj.pass_index = renderIdIdx
a