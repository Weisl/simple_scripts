import bpy

def create_clean_object_with_mesh(obj):
    if not obj or not obj.data:
        return

    # Store the original mesh data
    original_mesh = obj.data
    original_world_matrix = obj.matrix_world.copy()

    # Calculate the inverse of the original world matrix
    inverse_world_matrix = original_world_matrix.inverted()

    # Create a new mesh with vertices in object space
    new_mesh = bpy.data.meshes.new("CleanMesh")
    vertices = [inverse_world_matrix @ original_world_matrix @ v.co for v in original_mesh.vertices]
    polygons = [p.vertices for p in original_mesh.polygons]

    new_mesh.from_pydata(vertices, [], polygons)
    new_mesh.update()

    # Create a new object with the clean mesh
    new_obj = bpy.data.objects.new("CleanObject", new_mesh)

    # Link the new object to the scene
    bpy.context.collection.objects.link(new_obj)

    # Ensure the new object has clean transformation matrices
    new_obj.matrix_parent_inverse.identity()
    new_obj.matrix_basis.identity()
    new_obj.matrix_local.identity()

    # Position the new object at the original object's location
    new_obj.matrix_world = original_world_matrix

    return new_obj

# Run the function on the selected object
original_obj = bpy.context.object
new_obj = create_clean_object_with_mesh(original_obj)
