"""converts all non meshes to meshes, applies modifiers and merges all objects

import bpy
import os

# Use your own script name here:
filepath = "C:/Users/weisl/Documents/GitHub/mp_mini_script_utils/master/materialFromParent.py"
global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)

"""

import bpy
import re
import random

selectedObjects =  bpy.context.selected_objects.copy()

def makeMaterial(name, diffuse):
    b_mat_exists = False
    for mat in bpy.data.materials:
        if mat.name == name:
            b_mat_exists = True

    if b_mat_exists == False:
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = diffuse
    return mat


def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)


def get_children(ob, child_list):
    # recursive funtion to find all children
    for ob_child in bpy.data.objects:
        if ob_child.parent == ob:
            child_list.append(ob_child)
            chidesChild_list = []
            child_list = child_list + get_children(ob_child, chidesChild_list)
    return child_list


for obj in selectedObjects:

    if obj.type == 'EMPTY':
        if obj.parent == None:
            objectname = obj.name
            objectname = re.sub('^[A-Z][A-Z]_', '', objectname)  # regex Cut Prefix Away

            matName = "MI_" + objectname
            # matName.replace('_LP', '_MAT')

            if matName in bpy.data.materials:
                material = bpy.data.materials[matName]
            else:
                material = makeMaterial(matName, (random.random(), random.random(), random.random()))

            child_list = []
            child_list = get_children(obj,child_list)

            for child in child_list:
                if child.type == 'MESH' or child.type == 'CURVE' or child.type == 'SURFACE' or child.type == 'FONT' or child.type == 'META':
                    bpy.context.scene.objects.active = child

                    for i in range(0, len(obj.material_slots)):
                        obj.active_material_index = i
                        bpy.ops.object.material_slot_remove()
                        print ("entered")
                    setMaterial(child, material)






