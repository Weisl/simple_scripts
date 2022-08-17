"""
Slect objects for socket and than socket parent
Creates a SOCKET object for all selected Objects. The SOCKETS are parented to the active object.

# This stub runs a python script relative to the currently open
# blend file, useful when editing scripts externally.

import bpy
import os

# Use your own script name here:
filepath = "C:/Users/weisl/Documents/GitHub/mp_mini_script_utils/autoSocketCreation.py"
global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)
"""

import bpy

objects = bpy.context.selected_objects[:-1].copy()
activeObject = bpy.context.view_layer.objects.active.copy()

socketList = []

for obj in objects:
    if obj is not activeObject:
        emptyName = "SOCKET_" + obj.name
        if emptyName not in bpy.data.objects:
            if (obj.type == 'MESH' or obj.type == 'EMPTY') and obj is not activeObject:
                empty = bpy.data.objects.new("empty", None)
                bpy.context.scene.objects.link(empty)
                empty.location = (obj.location[0], obj.location[1], obj.location[2])
                empty.rotation_euler = (obj.rotation_euler[0], obj.rotation_euler[1], obj.rotation_euler[2])
                empty.scale = (obj.scale[0], obj.scale[1], obj.scale[2])

                empty.empty_draw_size = 15
                empty.empty_draw_type = 'SPHERE'

                empty.name = emptyName
                socketList.append(empty)

for obj in objects:
    obj.select = False
for obj in socketList:
    obj.select_set(True)

bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

for obj in objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = activeObject
