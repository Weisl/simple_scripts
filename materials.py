import bpy
import os

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


    #load BaseColor
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "../textures/"
    textureFolder = os.path.join(script_dir, rel_path)
    

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


bpy.context.area.type = 'TEXT_EDITOR'
