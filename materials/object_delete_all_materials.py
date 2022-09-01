"""Delete all material slots of active object"""

import bpy

for obj in bpy.data.objects:
    try:
        obj.data.materials.clear()
    except:
        print("")
