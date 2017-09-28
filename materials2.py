'''
Copyright (C) 2017 Matthias Patscheider
patscheider.matthias@mgail.com

Created by Matthias Patscheider

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Material Loading PBR",
    "description": "",
    "author": "Matthias Patscheider",
    "version": (0, 5, 0),
    "blender": (2, 79, 0),
    "location": "View3D",
    "warning": "beta",
    "wiki_url": "",
    "category": "Object" }


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

class LoadImagesPanel(bpy.types.Panel):
    bl_idname = "load_images"
    bl_label = "Load "
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        wm = context.window_manager

        layout = self.layout


        row = layout.row()
        row.prop(wm, "my_previews_dir")
        if wm.my_previews_dir == '' or wm.my_previews_dir is None:
            wm.my_previews_dir = str(bpy.path.abspath('//'))

        row = layout.row()
        row.operator("images.load", text = "loadImages")
        row = layout.row()
        row.operator("file.make_paths_relative", text = "realitve Paths")

class LoadImagesOp(bpy.types.Operator):
    bl_idname = "images.load"
    bl_label = "Load Images"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        wm = context.window_manager

        areType = bpy.context.area.type
        bpy.context.area.type = 'NODE_EDITOR'

        for mat in bpy.data.materials:

            texBName = ""
            texNName = ""
            texRName = ""
            texMName = ""
            rexIORName = ""

            mat.use_nodes = True

            nodes = mat.node_tree.nodes
            diffuse = nodes.get("Principled BSDF")

            # clear all nodes to start clean
            for node in nodes:
                nodes.remove(node)

            textureFolder = wm.my_previews_dir

            texBName = mat.name + "_B" + ".png"
            texNName = mat.name + "_N" + ".png"
            texRName = mat.name + "_R" + ".png"
            texMName = mat.name + "_M" + ".png"
            rexIORName = mat.name + "_IOR" + ".png"
            filepath_B = textureFolder + texBName
            filepath_N = textureFolder + texNName
            filepath_R = textureFolder + texRName
            filepath_M = textureFolder + texMName
            filepath_IOR = textureFolder + rexIORName

            # create principled node
            node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            node_principled.name = 'Principled'
            node_principled.inputs[0].default_value = (0, 1, 0, 1)  # green RGBA
            node_principled.inputs[1].default_value = 0  # strength
            node_principled.inputs[5].default_value = 1  # specular
            node_principled.location = -400, 0

            # create output node
            node_output = nodes.new(type='ShaderNodeOutputMaterial')
            node_output.name = 'Material Output'
            node_output.location = 0, 0

            node_baseColor = nodes.new(type='ShaderNodeTexImage')
            node_baseColor.name = 'texture_B'
            node_baseColor.location = -800, 400

            node_normal = nodes.new(type='ShaderNodeTexImage')
            node_normal.name = 'texture_N'
            node_normal.color_space = 'NONE'
            node_normal.location = -800, -400

            node_normalMap = nodes.new(type='ShaderNodeNormalMap')
            node_normalMap.name = 'normalMap'
            node_normalMap.inputs[0].default_value = 2
            node_normalMap.location = -600, -400

            node_roughness = nodes.new(type='ShaderNodeTexImage')
            node_roughness.name = 'texture_R'
            node_roughness.color_space = 'NONE'
            node_roughness.location = -800, 200

            node_metallic = nodes.new(type='ShaderNodeTexImage')
            node_metallic.name = 'texture_M'
            node_metallic.color_space = 'NONE'
            node_metallic.location = -800, 0

            node_ior = nodes.new(type='ShaderNodeTexImage')
            node_ior.name = 'texture_IOR'
            node_ior.color_space = 'NONE'
            node_ior.location = -800, -600

            try:
                texture_BaseColor = bpy.data.images.load(filepath_B, check_existing=True)
                texture_Normal = bpy.data.images.load(filepath_N, check_existing=True)
                texture_Roughness = bpy.data.images.load(filepath_R, check_existing=True)
                texture_Metalness = bpy.data.images.load(filepath_M, check_existing=True)



                '''if texBName in bpy.data.images:
                    bpy.data.images[texBName].reload()
                else:
                    texture_BaseColor = bpy.data.images.load(filepath_B, check_existing=False)

                if texNName in bpy.data.images:
                    bpy.data.images[texNName].reload()
                else:
                    texture_Normal = bpy.data.images.load(filepath_N, check_existing=False)

                if texRName in bpy.data.images:
                    bpy.data.images[texRName].reload()
                else:
                    texture_Roughness = bpy.data.images.load(filepath_R, check_existing=False)

                if texMName in bpy.data.images:
                    bpy.data.images[texMName].reload()
                else:
                    texture_Metalness = bpy.data.images.load(filepath_M, check_existing=False)
                    '''

                node_baseColor.image = texture_BaseColor
                node_normal.image = texture_Normal
                node_roughness.image = texture_Roughness
                node_metallic.image = texture_Metalness

            except:
                print("1111  Unexpected error:" + str(sys.exc_info()[0]))

            try:
                texture_IOR = bpy.data.images.load(filepath_IOR, check_existing=True)
                node_ior.image = texture_IOR
            except:
                print("2222  Unexpected error:" +  str(sys.exc_info()[0]))

            # link nodes
            links = mat.node_tree.links
            link = links.new(node_principled.outputs[0], node_output.inputs[0])
            link = links.new(node_baseColor.outputs[0], node_principled.inputs[0])
            link = links.new(node_roughness.outputs[0], node_principled.inputs[7])
            link = links.new(node_metallic.outputs[0], node_principled.inputs[4])
            link = links.new(node_normal.outputs[0], node_normalMap.inputs[1])
            link = links.new(node_normalMap.outputs[0], node_principled.inputs['Normal'])

        bpy.context.area.type = areType

        return {"FINISHED"}

def register():
    bpy.utils.register_class(LoadImagesPanel)
    bpy.utils.register_class(LoadImagesOp)

    WindowManager.my_previews_dir = StringProperty(
            name="Export Path",
            subtype='DIR_PATH',
            default=""
            )

def unregister():
    bpy.utils.unregister_class(LoadImagesPanel)
    bpy.utils.unregister_class(LoadImagesOp)

if __name__ == "__main__":
    register()
