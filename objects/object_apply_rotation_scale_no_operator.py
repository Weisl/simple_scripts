""" Apply scale without using an operator
    Ressources:
    - https://github.com/machin3io/MACHIN3tools/blob/9de036bf9ca0fed81ec36134101219d3b4f2c350/operators/apply.py#L52
    - https://blenderartists.org/t/apply-transform-and-rotation-without-ops/1217959
"""

import bpy
from mathutils import Vector, Matrix, Quaternion

obj = bpy.context.object

rotation = False
scale = True

def get_loc_matrix(location):
    return Matrix.Translation(location)

def get_rot_matrix(rotation):
    return rotation.to_matrix().to_4x4()

def get_sca_matrix(scale):
    scale_mx = Matrix()
    for i in range(3):
        scale_mx[i][i] = scale[i]
    return scale_mx

mx = obj.matrix_world
loc, rot, sca = mx.decompose()

# apply the current transformations on the mesh level
if rotation and scale:
    mesh_matrix = get_rot_matrix(rot) @ get_sca_matrix(sca)
elif rotation:
    mesh_matrix = get_rot_matrix(rot)
elif scale:
    mesh_matrix = get_sca_matrix(sca)

obj.data.transform(mesh_matrix)

if rotation and scale:
    apply_matrix = get_loc_matrix(loc) @ get_rot_matrix(Quaternion()) @ get_sca_matrix(Vector.Fill(3, 1))
elif rotation:
    apply_matrix = get_loc_matrix(loc) @ get_rot_matrix(Quaternion()) @ get_sca_matrix(sca)
elif scale:
    apply_matrix = get_loc_matrix(loc) @ get_rot_matrix(rot) @ get_sca_matrix(Vector.Fill(3, 1))

apply_matrix = get_loc_matrix(loc) @ get_rot_matrix(rot) @ get_sca_matrix(Vector.Fill(3, 1))
obj.matrix_world = apply_matrix

