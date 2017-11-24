import bpy

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

def deleteAllMaterials(ob):
    ob.data.materials.clear()
