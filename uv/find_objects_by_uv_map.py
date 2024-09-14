import bpy

# Replace 'UVMap_Name' with the name of the UV map you're looking for
target_uv_map_name = 'UVMap_Name'

print(f"Objects with UV map '{target_uv_map_name}':")

# Iterate through all objects in the scene
for obj in bpy.context.scene.objects:
    # Check if the object is a mesh and has UV maps
    if obj.type == 'MESH' and obj.data.uv_layers:
        # Check if any of the UV layers match the target UV map name
        for uv_layer in obj.data.uv_layers:
            if uv_layer.name == target_uv_map_name:
                print(obj.name)
                break  # No need to check other UV maps for this object
