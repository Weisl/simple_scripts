'''Assigns a RenderID to the selected Objects. Render id can be changed by changing renderIdIdx '''
import bpy

renderIdIdx = 1

selected_objects = bpy.context.selected_objects.copy()
for obj in selected_objects:
    obj.pass_index = renderIdIdx
