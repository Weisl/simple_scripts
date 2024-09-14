import bpy

# Replace 'Material_Name' with the name of the material you're looking for
target_material_name = 'Material_Name'

# Find the material object from the name
target_material = bpy.data.materials.get(target_material_name)

if target_material is None:
    print(f"Material '{target_material_name}' not found.")
else:
    print(f"Objects using the material '{target_material_name}':")

    # Iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
        # Check if the object has material slots
        if obj.type == 'MESH':  # Checking if the object is a mesh
            for slot in obj.material_slots:
                if slot.material == target_material:
                    print(obj.name)
