'''parent selected objects to empty objects'''

import bpy

for obj in bpy.context.selected_objects:
    originalPosition = list(obj.location)
    originalRotaiton = list(obj.rotation_euler)
    originalScale = list(obj.scale)

    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)

    empty = bpy.data.objects.new("empty", None)
    bpy.context.scene.objects.link(empty)
    empty.empty_draw_size = 200
    empty.empty_draw_type = 'SPHERE'

    empty.location = (0, 0, 0)

    obj.parent = empty

    empty.location = originalPosition
    empty.rotation_euler = originalRotaiton
    empty.scale = originalScale
