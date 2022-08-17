"""creates material from objectname"""
import bpy

materialSuffix = ""
materialPrefix = "MA_"

# TODO:
replaceSuffix = ""
replacePrefix = ""


def makeMaterial(name, diffuse):
    """ creates a material if it doesn't exist yet """
    b_mat_exists = False
    for mat in bpy.data.materials:
        if mat.name == name:
            b_mat_exists = True

    if b_mat_exists == False:
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = diffuse
    return mat


def setMaterial(ob, mat):
    """append material to object"""
    me = ob.data
    me.materials.append(mat)


for obj in bpy.context.selected_objects:
    """ """
    if obj.type == 'MESH':
        matName = materialPrefix + obj.name + materialSuffix # matName.replace('_LP', '_MAT')

        if matName in bpy.data.materials:
            for mat in bpy.data.materials:
                if mat.name == matName:
                    material = mat
        else:
            material = makeMaterial(matName, (0.8, 0.8, 0.8, 1.0))

        setMaterial(obj, material)



