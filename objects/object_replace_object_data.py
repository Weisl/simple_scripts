"""Replace mesh data_a with mesh data_b for all selected objects """
import bpy

data_a = ""
data_b = ""

# checks if object exists
for data in bpy.data.meshes:
    if data.name == data_a:
        data_b = data
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.data = data
else:
    ("Data doesn not exist")
