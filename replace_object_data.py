import bpy 

data_name = "column_railing.008"
new_data_name = "column_railing.011"


for obj in bpy.context.selectable_objects:
    if obj.type == 'MESH':
        for data in bpy.data.meshes:
            if data.name == new_data_name:
                obj.data = data