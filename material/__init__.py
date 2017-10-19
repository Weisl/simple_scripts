'''
Copyright (C) 2017 Matthias Patscheider
patscheider.matthias@gmail.com

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
    "name": "My Addon Name",
    "description": "",
    "author": "Your Name",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object" }


import bpy
import bpy
import os

from bpy.types import Operator, AddonPreferences
import bpy.props as prop
from bpy.types import Scene
from bpy.types import WindowManager
from bpy.props import (
    StringProperty,
    EnumProperty,
    BoolProperty,
    FloatProperty,
    IntProperty,
    CollectionProperty,
    BoolVectorProperty
    )
# load and reload submodules
##################################

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())


# panel
##################################
class TextureImport(bpy.types.Panel):
    bl_idname = "texture_import"
    bl_label = "Texture Import"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "category"

    def draw(self, context):
        layout = self.layout

        #if wm.texture_imagePath == '' or wm.texture_imagePath is None:
         #   wm.texture_imagePath = str(bpy.path.abspath('//'))

        row = layout.row()
        row.prop(wm, "texture_imagePath")
        row = layout.row()
        row.scale_y = 2.0

        row = layout.row()
        row.prop(wm, "textureimport_channel")

        row.operator("my_operator.create_nodes", text = "ImportTextures")
        """     
        bpy.context.area.type = 'NODE_EDITOR'
        wm = bpy.context.window_manager
        wm = wm.texture_imagePath
        
        for mat in bpy.data.materials:
            for texturechannel in wm.
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


            #load BaseColor
            textureFolder = "G:/01_Dropbox/Dropbox/projects/2017_veniceProject/020_Production/assets/cathedral/texturing/substance/"
            texBName = mat.name + "_B" + ".png"
            texNName = mat.name + "_N" + ".png"
            texRName = mat.name + "_R" + ".png"
            texMName = mat.name + "_M" + ".png"
            rexIORName = mat.name + "_IOR" + ".png"
            filepath_B = textureFolder + "2k/" + texBName
            filepath_N = textureFolder + "2k/" + texNName
            filepath_R = textureFolder + "2k/" + texRName
            filepath_M = textureFolder + "2k/" + texMName
            filepath_IOR = textureFolder + "2k/" + rexIORName
            #texture_Normal = bpy.data.images.load(filepath_N, check_existing=False)
            #texture_Roughness = bpy.data.images.load(filepath_R, check_existing=False)
            #texture_Metalness = bpy.data.images.load(filepath_M, check_existing=False)


            # create principled node
            node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            node_principled.name = 'Principled'
            node_principled.inputs[0].default_value = (0,1,0,1)  # green RGBA
            node_principled.inputs[1].default_value = 0 # strength
            node_principled.inputs[5].default_value = 1  # specular
            node_principled.location = -400,0

            # create output node
            node_output = nodes.new(type='ShaderNodeOutputMaterial')
            node_output.name = 'Material Output'
            node_output.location = 0,0

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

            #node_height = nodes.new(type='ShaderNodeTexImage')
            #node_height.name = 'texture_H'
            #node_normal.color_space = 'NONE'
            #node_height.location = -800, -200

            #node_emissive = nodes.new(type='ShaderNodeTexImage')
            #node_emissive.name = 'texture_E'
            #node_emissive.location = -800, -400

            #node_ambientOcclussion= nodes.new(type='ShaderNodeTexImage')
            #node_ambientOcclussion.name = 'texture_AO'
            #node_normal.color_space = 'NONE'
            #node_ambientOcclussion.location = -800, -400
            #create texture nodes


            try:
                texture_BaseColor = bpy.data.images.load(filepath_B, check_existing=False)
                texture_Normal = bpy.data.images.load(filepath_N, check_existing=False)
                texture_Roughness = bpy.data.images.load(filepath_R, check_existing=False)
                texture_Metalness = bpy.data.images.load(filepath_M, check_existing=False)

                node_baseColor.image = texture_BaseColor
                node_normal.image = texture_Normal
                node_roughness.image = texture_Roughness
                node_metallic.image = texture_Metalness

            except:
                print(" ")

            try:
                texture_IOR = bpy.data.images.load(filepath_IOR, check_existing=False)
                node_ior.image = texture_IOR
            except:
                print(" ")

            # link nodes
            links = mat.node_tree.links
            link = links.new(node_principled.outputs[0], node_output.inputs[0])
            link = links.new(node_baseColor.outputs[0], node_principled.inputs[0])
            link = links.new(node_roughness.outputs[0], node_principled.inputs[7])
            link = links.new(node_metallic.outputs[0], node_principled.inputs[4])
            #link = links.new(node_height.outputs[0], node_principled.inputs[2])
            #link = links.new(node_emissive.outputs[0], node_principled.inputs[3])
            link = links.new(node_normal.outputs[0], node_normalMap.inputs[1])
            link = links.new(node_normalMap.outputs[0], node_principled.inputs['Normal'])
            #link = links.new(node_ambientOcclussion.outputs[0], node_principled.inputs[4])
            (bpy.context.area.type = 'TEXT_EDITOR') """


class TextureMap():
    bl_idname = "texture.channelmap"

    def __init__(self, channelType, colorSpace = srgb):
        self.channelType = channelType
        self.colorSpace = srgb



class CreateNodes(bpy.types.Operator):
    bl_idname = "my_operator.create_nodes"
    bl_label = "Create Nodes"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True



    def execute(self, context):
        print ("hallo welt")
        return {"FINISHED"}



#userPreferences
############
class ExportPreferences(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__  ### __package__ works on multifile and __name__ not

    filepath = StringProperty(
            name="Example File Path",
            subtype='FILE_PATH',
            )
    number = IntProperty(
            name="Example Number",
            default=4,
            )
    boolean = BoolProperty(
            name="Example Boolean",
            default=False,
            )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Export Info")
        box.prop(self, "filepath")
        box.prop(self, "number")
        box.prop(self, "boolean")

        box.label(text="Export Settings")
##################################
# register
##################################

import traceback

def register():
    # TODO: add custom (channels)
    WindowManager.textureimport_channel = EnumProperty(
        items=(('ALBEDO', "Albedo", "contains color data without lighting information "), # TODO Option for transparency
                ('ROUGHNESS', "Roughness", "roughness map"),
                ('METALNESS', "Metalness", "metalness map"),
                ('EMISSIVE', "Emissive","emissive map"),
                ('NORMAL', "Normal","normal"), #TODO Option OpenGL or Direct x
                ('MR',"MetalRough", "ChannelPackedTexture")
                ),
        name="Texture Maps",
        options={'ENUM_FLAG'},
        description="IChoose the used Channels",
        default={'ALBEDO', 'ROUGHNESS', 'METALNESS'},
        )

    WindowManager.textureimport_channel = EnumProperty(
        items=(('JPG', "Jpg", ""),
                ('PNG', "PNG", ""),
                ('TIFF', "TIFF", ""),
                ('PSD', "PSD","")
                ),
        name="Texture Format",
        description="IChoose the used Channels",)


    WindowManager.texture_imagePath = StringProperty(
        name="image path",
        subtype='DIR_PATH',
        default=""
        )

    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()

    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

def unregister():
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    print("Unregistered {}".format(bl_info["name"]))
