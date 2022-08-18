"""deselects all empties"""

import bpy

for obj in bpy.context.selected_objects:
    if obj.type == 'EMPTY':
        obj.select_set(False)
