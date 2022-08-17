"""deselects all empties"""

import bpy

for obj in bpy.context.selected_objects:
    if obj.type == 'EMPTY':
        print (obj)
        obj.select = False