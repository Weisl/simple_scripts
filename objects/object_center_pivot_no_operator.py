""" Center pivot without using an operator"""
import bpy
import mathutils

from mathutils import Matrix, Vector

def set_origin_to_center(obj, center_point):
    obj.data.transform(mathutils.Matrix.Translation(-center_point))
    obj.location += center_point


obj = bpy.context.object

x, y, z = [sum([(obj.matrix_world.inverted() @ v.co)[i] for v in obj.data.vertices]) for i in range(3)]
count = float(len(obj.data.vertices))
center = obj.matrix_world @ (Vector((x, y, z)) / count)

set_origin_to_center(obj, center)