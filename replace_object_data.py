import bpy
"""replaces mesh data for all selected objects """

new_data_name = "column_railing.011"

new_mesh_data = "";
#checks if object exists
for data in bpy.data.meshes:
    if data.name == new_data_name:
        
        new_mesh_data = data

        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                obj.data = data
else:
    ("Data doesn not exist") 
