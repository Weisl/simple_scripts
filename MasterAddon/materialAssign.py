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

from .funcMat import makeMaterial, setMaterial, deleteAllMaterials
from .func import get_children

class AssetCreate(bpy.types.Operator):
    bl_idname = "master.assign_material"
    bl_label = "Assign Material"
    bl_description = "Assign Asset Material"
    bl_options = {'REGISTER', 'UNDO'}

    my_remove = bpy.props.BoolProperty(name="Replace Materials", default=True)


    @classmethod
    def poll(cls, context):
        if bpy.context.selected_objects == None:
            return False
        return True

    def execute(self, context):
        selection = bpy.context.selected_objects.copy()
        assetList = main(self, selection)
        return {"FINISHED"}

def main(self,selection):
    for obj in selection:

        if obj.type == 'EMPTY':
            if obj.parent == None:
                objectname = obj.name
                objectname = re.sub('^[A-Z][A-Z]_', '', objectname)  # regex Cut Prefix Away

                matName = "MI_" + objectname
                matName = matName.replace("edit_", "")
                # matName.replace('_LP', '_MAT')

                if matName in bpy.data.materials:
                    material = bpy.data.materials[matName]
                else:
                    material = makeMaterial(matName, (random.random(), random.random(), random.random()))

                child_list = []
                child_list = get_children(obj, child_list)

                for child in child_list:
                    if self.my_remove == True and child.type != 'EMPTY':
                        deleteAllMaterials(child)

                    if child.type == 'MESH' or child.type == 'CURVE' or child.type == 'SURFACE' or child.type == 'FONT' or child.type == 'META':
                        bpy.context.scene.objects.active = child

                        for i in range(0, len(obj.material_slots)):
                            obj.active_material_index = i
                            bpy.ops.object.material_slot_remove()
                            print ("entered")
                        setMaterial(child, material)






