"""
Slect objects for socket and than socket parent
Creates a SOCKET object for all selected Objects. The SOCKETS are parented to the active object.
"""

import bpy

for obj in bpy.context.selected_objects:
    emptyName = "SOCKET_" + obj.name
    if emptyName not in bpy.data.objects:
        if obj.type == 'MESH':
            empty = bpy.data.objects.new("empty", None)
            bpy.context.scene.objects.link(empty)
            empty.location = (obj.location[0], obj.location[1], obj.location[2])
            empty.empty_draw_size = 100
            empty.name = emptyName

            empty.parent = bpy.context.active_object

