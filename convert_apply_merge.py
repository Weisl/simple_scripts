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

def duplicateObject(ob):
    bpy.context.scene.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT')

    me = ob.data # use current object's data
    me_copy = me.copy()

    new_ob = bpy.data.objects.new(ob.name + "_Copy", me_copy)
    new_ob.matrix_world  = ob.matrix_world 
    

    bpy.ops.object.mode_set(mode = 'OBJECT')
           
    scene = bpy.context.scene
    scene.objects.link(new_ob)
    scene.update()
    
    new_ob.select = True
    bpy.context.scene.objects.active = ob
    bpy.ops.object.make_links_data(type='MODIFIERS')
    bpy.ops.object.make_links_data(type='MATERIAL')
    
    return new_ob


def applyMod(obj):
    bpy.ops.object.select_all(action='DESELECT')
    
    bpy.context.scene.objects.active = obj
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

active_object = bpy.context.scene.objects.active
mergedObject_list = []

for obj in bpy.context.selected_objects:
    # only count objects without parent
    if obj.parent == None:
        dupli_list = []

        # new object
        me = bpy.data.meshes.new(obj.name + "_data")
        mergedObject = bpy.data.objects.new(obj.name + "_clone", me)
        mergedObject.location = obj.location
        mergedObject.rotation_euler = mergedObject.rotation_euler

        scn = bpy.context.scene
        scn.objects.link(mergedObject)

        child_list = []
        child_list = get_children(obj,child_list)
        socket_list = []

        for obj in child_list:
            if obj.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
                dupli_list.append(duplicateObject(obj))
                print ("object " + obj.name)
            elif obj.type == 'EMPTY' and obj.name.startswith("socket_"):
                empty = bpy.data.objects.new(obj.name.replace("socket", "SOCKET") ,None)

                scene = bpy.context.scene
                scene.objects.link(empty)

                empty.location = (0,0,0)
                empty.rotation_euler = obj.rotation_euler
                empty.scale = obj.scale
                empty.empty_draw_type = obj.empty_draw_type
                empty.empty_draw_size = obj.empty_draw_size
                socket_dic = {'oldSocket': obj, 'newSocket': empty}
                socket_list.append(socket_dic)




        for obj in dupli_list:
            obj.select = True
            bpy.context.scene.objects.active = obj
            bpy.ops.object.make_local(type='ALL')
            bpy.ops.object.make_single_user(object=True, obdata=True, material=False, texture=False, animation=False)


            # convert spline
            if obj.type != 'MESH':
                old_obj = obj

                scene = bpy.context.scene
                print (old_obj.name)

                #create new data and obj
                me = old_obj.to_mesh(scene, False, 'PREVIEW')
                new_obj = bpy.data.objects.new(old_obj.name + "_new", me)
                new_obj.matrix_world = old_obj.matrix_world
                scene.objects.link(new_obj)

                mod_obj = old_obj         # cube with mods
                modable_obj = new_obj   # cube without mods

                bpy.ops.object.select_all(action='DESELECT')

                mod_obj.select = True
                bpy.context.scene.objects.active = mod_obj
                modable_obj.select = True

                bpy.ops.object.make_links_data(type='MODIFIERS')
                bpy.ops.object.select_all(action='DESELECT')


                scene.objects.unlink(old_obj)
                dupli_list.append(new_obj)

                bpy.context.scene.objects.active = new_obj
                obj = new_obj

            applyMod(obj)

        bpy.ops.object.select_all(action='DESELECT')
        mergedLayer_list = [False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False]

        for ob in dupli_list:
            ob.select = True
        bpy.context.scene.objects.active = mergedObject
        mergedObject.select = True

        mergedObject_list.append(mergedObject)
        bpy.ops.object.join()

        for socket_dic in socket_list:
            socket = socket_dic["newSocket"]
            oldSocket = socket_dic["oldSocket"]

            socket.location = oldSocket.location
            socket.rotation_euler = oldSocket.rotation_euler
            socket.scale = oldSocket.scale

            socket.select = True
            socket.layers = mergedLayer_list
        bpy.context.scene.layers[10] = True
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)


for obj in mergedObject_list:
    print ("entered " + obj.name)
    bpy.context.scene.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT')
    mergedObject.layers = mergedLayer_list




