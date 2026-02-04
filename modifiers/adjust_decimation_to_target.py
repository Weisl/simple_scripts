"""
Blender Script: Adjust Decimation to Target Triangle Count

Description:
This script adds a decimate modifier to the active mesh object in Blender and adjusts the modifier's ratio to reduce the triangle count to below a specified target. The script uses a binary reduction approach, halving the decimate ratio in each iteration until the target triangle count is achieved or the ratio can no longer be reduced.

Usage:
1. Open Blender and load your mesh object.
2. Select the mesh object you want to decimate.
3. Open the Scripting workspace in Blender.
4. Create a new script and paste this code.
5. Run the script.

The script will print the current triangle count and ratio during each iteration, providing feedback on the decimation process.
"""

import bpy

def adjust_decimation(target_triangles):
    # Ensure there is an active object and it is a mesh
    if bpy.context.active_object and bpy.context.active_object.type == 'MESH':
        obj = bpy.context.active_object

        # Add a decimate modifier
        decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
        decimate.decimate_type = 'COLLAPSE'

        # Start with a ratio that is likely too high
        ratio = 1.0

        # Loop to adjust the ratio
        while ratio > 0.01:
            decimate.ratio = ratio

            # Use the dependency graph to get the evaluated mesh
            depsgraph = bpy.context.evaluated_depsgraph_get()
            obj_eval = obj.evaluated_get(depsgraph)
            mesh_from_eval = obj_eval.to_mesh()

            # Calculate the current number of triangles
            current_triangles = sum(len(poly.vertices) - 2 for poly in mesh_from_eval.polygons)
            print(f"Current triangles: {current_triangles}, Ratio: {ratio}")

            # Free the evaluated mesh to prevent memory leaks
            obj_eval.to_mesh_clear()

            # Check if the current triangle count is below the target
            if current_triangles < target_triangles:
                print("Target triangle count achieved.")
                break

            # If not, halve the ratio
            ratio /= 2

        if current_triangles >= target_triangles:
            print("Could not reduce triangles below target with ratio > 0.01.")

    else:
        print("No active mesh object selected.")

# Call the function to adjust the decimation
adjust_decimation(256)
