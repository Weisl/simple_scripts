'''
import bpy
import os

# Use your own script name here:
filename = "toggleWireframes.py"

import os
pathMiniScripts = "Documents/GitHub/mp_mini_script_utils/"
documents = os.path.join(os.path.join(os.environ['USERPROFILE']), pathMiniScripts)
filepath = os.path.join(documents, filename)

global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)


'''

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
