import bpy


def rename_objects_in_active_collection():
    # Get the active collection
    active_collection = bpy.context.view_layer.active_layer_collection.collection

    # Create a dictionary to group objects by their data (mesh or curve)
    data_dict = {}

    # Filter objects in the active collection by type MESH and CURVE, and group by their data
    for obj in active_collection.objects:
        if obj.type in {'MESH', 'CURVE'}:
            data_key = obj.data
            if data_key not in data_dict:
                data_dict[data_key] = []
            data_dict[data_key].append(obj)

    # Process each group of objects sharing the same data
    for obj_list in data_dict.values():
        if len(obj_list) > 0:
            # Rename the first object with o_ prefix (original)
            original_object = obj_list[0]
            original_name = original_object.name
            original_object.name = f"o_{original_name}"

            # Rename all other objects with i_ prefix (instance)
            for obj in obj_list[1:]:
                obj.name = f"i_{original_name}"


# Run the renaming function for the active collection
rename_objects_in_active_collection()
