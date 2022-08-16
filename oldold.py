"""converts all non meshes to meshes, applies modifiers and merges all objects

import bpy
import os

# Use your own script name here:
filepath = "C:/Users/weisl/Documents/GitHub/mp_mini_script_utils/convert_apply_merge.py"
global_namespace = {"__file__": filepath, "__name__": "__main__"}
with open(filepath, 'rb') as file:
    exec(compile(file.read(), filepath, 'exec'), global_namespace)

"""

import bpy,bmesh
from .func import *

selection = bpy.context.selected_objects.copy()
mergedObject_list = []
assetPre = "edit_"


def applyMod(obj):
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode = 'OBJECT')

    if obj is not None:
        for modi in obj.modifiers:
            try:
                midifiername = modi.name
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier = midifiername)
            except (RuntimeError):
                 obj.modifiers.remove(modi)
    
    
def get_children(ob, child_list):
    # recursive funtion to find all children
    for ob_child in bpy.data.objects:
        if ob_child.parent == ob:
            child_list.append(ob_child)
            chidesChild_list = []
            child_list = child_list + get_children(ob_child, chidesChild_list)
    return child_list


def convertToMesh(obj):
    old_obj = obj

    scene = bpy.context.scene
    print (old_obj.name)

    # create new data and obj
    me = old_obj.to_mesh(scene, False, 'PREVIEW')
    new_obj = bpy.data.objects.new(old_obj.name + "_new", me)
    new_obj.matrix_world = old_obj.matrix_world
    scene.objects.link(new_obj)

    mod_obj = old_obj  # cube with mods
    modable_obj = new_obj  # cube without mods

    bpy.ops.object.select_all(action='DESELECT')

    mod_obj.select = True
    bpy.context.view_layer.objects.active = mod_obj
    modable_obj.select = True

    bpy.ops.object.make_links_data(type='MODIFIERS')
    bpy.ops.object.select_all(action='DESELECT')

    scene.objects.unlink(old_obj)
    bpy.context.view_layer.objects.active = new_obj
    applyMod(new_obj)

    return new_obj

active_object = bpy.context.view_layer.objects.active

# Convert instanced Groups!
for obj in selection:
    if obj.dupli_group == None:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.make_local(type='ALL')
        bpy.ops.object.duplicates_make_real(use_base_parent=True, use_hierarchy=False)
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, texture=False, animation=False)

for obj in selection:
    # only count objects without parent
    if obj.parent == None:
        dupli_list = []
        collision_list = []

        # save object names

        if obj.name.startswith(assetPre):
            assetName = obj.name.replace(assetPre, "")
        else:
            assetName = obj.name

        obj.name = assetPre + assetName

        # new object
        me = bpy.data.meshes.new(assetName + "_data")
        mergedObject = bpy.data.objects.new(assetName, me)
        mergedObject.location = obj.location
        mergedObject.rotation_euler = mergedObject.rotation_euler

        scn = bpy.context.scene
        scn.objects.link(mergedObject)

        child_list = []
        child_list = get_children(obj, child_list)
        socket_list = []

        # include linked Groups


        for obj in child_list:
            if obj.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
                if obj.name.startswith("UBX") or obj.name.startswith("UCX") or obj.name.startswith("edit_UBX") or obj.name.startswith("edit_UCX"):
                    collision_list.append(duplicateObject(obj))
                else:
                    dupli_list.append(duplicateObject(obj))

            elif obj.type == 'EMPTY' and obj.name.startswith("SOCKET_") or obj.name.startswith("edit_SOCKET_"):
                socketName = obj.name
                socketName = socketName.replace("edit_","")
                obj.name = assetPre + socketName
                empty = bpy.data.objects.new(socketName ,None)

                scene = bpy.context.scene
                scene.objects.link(empty)

                empty.location = (0,0,0)
                empty.rotation_euler = obj.rotation_euler
                empty.scale = obj.scale
                empty.empty_draw_type = obj.empty_draw_type
                empty.empty_draw_size = obj.empty_draw_size
                socket_dic = {'oldSocket': obj, 'newSocket': empty}
                socket_list.append(socket_dic)

        for obj in collision_list:
            obj.draw_type = 'WIRE'
            if obj.type != 'MESH':
                new_obj = convertToMesh(obj)
                collision_list.append(new_obj)
            else:
                applyMod(obj)

        for obj in dupli_list:
            obj.select = True
            # convert spline
            if obj.type != 'MESH':
                new_obj = convertToMesh(obj)
                dupli_list.append(new_obj)
            else:
                applyMod(obj)

        bpy.ops.object.select_all(action='DESELECT')
        mergedLayer_list = [False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False]

        # merge Objects
        for ob in dupli_list:
            ob.select = True
        bpy.context.view_layer.objects.active = mergedObject
        mergedObject.select = True

        mergedObject_list.append(mergedObject)
        bpy.ops.object.join()


        for socket_dic in socket_list:
            #print ("6")
            socket = socket_dic["newSocket"]
            oldSocket = socket_dic["oldSocket"]

            socket.matrix_world = oldSocket.matrix_world

            socket.select = True
            socket.layers = mergedLayer_list
        bpy.context.scene.layers[10] = True


        for col in collision_list:
            col.layers = mergedLayer_list
            col.select = True

        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

for obj in mergedObject_list:
    #print ("7")
    print ("entered " + obj.name)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.data.use_auto_smooth = True
    mergedObject.layers = mergedLayer_list




