"""Toggle between texture and wire view for all selected objects """

import bpy

selectedObjects = bpy.context.selected_objects.copy()

wire = 0
texture = 0

for ob in selectedObjects:
    if bpy.context.object.display_type == 'WIRE':
        wire = wire + 1
    else:
        texture = texture + 1
if wire == 0 or (wire != 0 and texture != 0):
    for ob in selectedObjects:
        bpy.context.view_layer.objects.active = ob
        bpy.context.object.display_type = 'WIRE'
else:
    for ob in selectedObjects:
        bpy.context.view_layer.objects.active = ob
        bpy.context.object.display_type = 'TEXTURED'

print("Finished")
