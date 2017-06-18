import bpy 
import re

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


for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        objectname = obj.name 
        objectname = re.sub('^[A-Z][A-Z]_', '', objectname) #regex Cut Prefix Away

        matName = "MI_" + objectname
        #matName.replace('_LP', '_MAT')
        
        if matName in bpy.data.materials:
            for mat in bpy.data.materials:
                if mat.name == matName:
                    material = mat
        else:
            material = makeMaterial(matName, (0.8,0.8,0.8))
            
        setMaterial(obj, material)
    
        

