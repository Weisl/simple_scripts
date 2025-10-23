import bpy
def fix_parent_inverse_matrix_decomposed(obj):
    if not obj.parent:
        return

    mesh = obj.data
    # Store the original world matrix
    ob_matrix_orig = obj.matrix_world.copy()
    # Calculate the "reverse_inverse_matrix"
    reverse_inverse_matrix = obj.parent.matrix_world.inverted() @ ob_matrix_orig

    # Decompose the matrix into location, rotation, and scale
    loc, rot, sca = reverse_inverse_matrix.decompose()

    # Construct matrices for each component
    loc_matrix = Matrix.Translation(loc)
    rot_matrix = rot.to_matrix().to_4x4()
    sca_matrix = Matrix.Scale(sca[0], 4, (1, 0, 0)) @ \
                 Matrix.Scale(sca[1], 4, (0, 1, 0)) @ \
                 Matrix.Scale(sca[2], 4, (0, 0, 1))

    # Apply location, rotation, and scale to the mesh vertices
    transformed_vertices = [loc_matrix @ rot_matrix @ sca_matrix @ v.co for v in mesh.vertices]
    mesh.vertices.foreach_set("co", [coord for v in transformed_vertices for coord in v])

    # Reset parent inverse matrix
    obj.matrix_parent_inverse.identity()
    # Reset the object's basis and local matrices
    obj.matrix_basis.identity()
    obj.matrix_local.identity()

    # Update the mesh
    mesh.update()

obj = bpy.context.object
_fix_collider_transform(obj)
