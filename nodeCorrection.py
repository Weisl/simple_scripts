'''
import bpy
import os

# Use your own script name here:
filepath = "C:/Users/weisl/Documents/GitHub/mp_mini_script_utils/nodeCorrection.py"
global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)
'''


import os
import sys

from os.path import *


import bpy
from bpy.types import Operator
from bpy.types import WindowManager
from bpy.types import Scene
from pathlib import Path
from bpy.props import (
    StringProperty,
    EnumProperty,
    BoolProperty,
    FloatProperty,
    IntProperty
    )



areType = bpy.context.area.type
bpy.context.area.type = 'NODE_EDITOR'
bpy.context.space_data.tree_type = 'ShaderNodeTree'


for mat in bpy.data.materials:
    mat.use_nodes = True    # make node accessable


    nodes = mat.node_tree.nodes

    for node in nodes:
        if node.type == "SEPRGB":
            nodes.remove(node)

    node_sepRGB = nodes.new(type='ShaderNodeSeparateRGB')
    node_sepRGB.name = 'separate_RGB'
    node_sepRGB.location = -600, -200

    princNode = None
    texNode = None

    for node in nodes:
        if node.type == "TEX_IMAGE":
            if node.image is not None:
                if node.image.filepath.endswith("_M.png"):
                    texNode = node
                    print("texImage" + mat.name)

        if node.type == "BSDF_PRINCIPLED":
            print ("principles" + mat.name)
            princNode = node

    if princNode is not None and texNode is not None:
        print("link")
        links = mat.node_tree.links

        #C.object.material_slots[0].material.node_tree.links.new(
        #    C.object.material_slots[0].material.node_tree.nodes[7].outputs[0],
        #    C.object.material_slots[0].material.node_tree.nodes[8].inputs[2])
        link = links.new(node_sepRGB.outputs[1], princNode.inputs[7])
        link = links.new(node_sepRGB.outputs[2], princNode.inputs[4])
        link = links.new(texNode.outputs[0], node_sepRGB.inputs[0])

bpy.context.area.type = areType