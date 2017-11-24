import bpy,bmesh

from .func import applyMod, duplicateObject, get_children, convertToMesh
from .assets import colliderEnum

def getActiveSelected ():
    oldActive = bpy.context.scene.objects.active
    oldSelection = bpy.context.selected_objects.copy()
    return oldActive, oldSelection

def setActiveSelected (oldActive, oldSelection):
    bpy.context.scene.objects.active = oldActive
    for obj in bpy.data.objects:
        obj.select = False
    for ob in oldSelection:
        ob.select = True


def mergeObjects(mergeTarget, mergeSelection):
    oldActive, oldSelection = getActiveSelected()

    print("MERGE SELECTION " + str(mergeSelection))
    bpy.context.scene.objects.active = mergeTarget

    for obj in bpy.data.objects:
        obj.select = False

    mergeTarget.select = True
    for ob in mergeSelection:
        ob.select = True

    bpy.ops.object.join()

    setActiveSelected(oldActive, oldSelection)
    return mergeTarget



class converApplyMerge(bpy.types.Operator):
    bl_idname = "master.conver_apply_merge"
    bl_label = "Conver Apply Merge"
    bl_description = ""
    bl_options = {"REGISTER"}

    my_autoSmooth = bpy.props.FloatProperty(name="Auto Smooth Angle", default=15)

    @classmethod
    def poll(cls, context):
        return bpy.context.scene.objects.active

    def execute(self, context):
        main(self,context)
        return {"FINISHED"}

def main(self,context):
    selection = bpy.context.selected_objects.copy()
    active_object = bpy.context.scene.objects.active

    mergedObject_list = []
    assetSuffix = "_edit"
    duplicateSuffix = "_dupl"


    mergedLayer_list = [False, False, False, False, False, False, False, False, False, False, True, False, False, False,
                        False, False, False, False, False, False]

    # Convert instanced Groups!
    for obj in selection:
        if obj.dupli_group == None:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.make_local(type='ALL')
            bpy.ops.object.duplicates_make_real(use_base_parent=True, use_hierarchy=False)
            bpy.ops.object.make_single_user(object=True, obdata=True, material=False, texture=False, animation=False)



    for obj in selection:
        # only count objects without parent
        if obj.parent == None:
            dupli_list = []

            # save object names

            if obj.name.endswith(assetSuffix):
                assetName = obj.name.replace(assetSuffix, "")
            else:
                assetName = obj.name

            obj.name = assetName + assetSuffix

            # new object
            me = bpy.data.meshes.new(assetName + "_data")
            mergedObject = bpy.data.objects.new(assetName, me)
            mergedObject.location = obj.location
            mergedObject.rotation_euler = mergedObject.rotation_euler

            scn = bpy.context.scene
            scn.objects.link(mergedObject)

            child_list = []
            child_list = get_children(obj, child_list)


            # include linked Groups


            for obj in child_list:                                          # works
                if obj.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
                    if obj.name.startswith(tuple(colliderEnum.getTuple())) == False:
                        newObj = duplicateObject(obj, duplicateSuffix)
                        dupli_list.append(newObj)

                    else:           ##### collider ####
                        objCollision = duplicateObject(obj, duplicateSuffix)
                        if obj.type != 'MESH':
                            objCollision = convertToMesh(obj)
                        else:
                            applyMod(obj)


                        oldObjectname = obj.name

                        if obj.name.endswith(assetSuffix) == False:
                            obj.name = obj.name + assetSuffix
                        objCollision.name = oldObjectname.replace(assetSuffix, "")
                        objCollision.parent = mergedObject
                        objCollision.matrix_local = obj.matrix_local
                        objCollision.draw_type = 'WIRE'
                        objCollision.layers = mergedLayer_list



                elif obj.type == 'EMPTY' and obj.name.startswith("SOCKET_"): ##### socket #####
                    socketName = obj.name                           #new socket name
                    socketName = socketName.replace(assetSuffix,"")

                    obj.name = socketName + assetSuffix             # old socket name

                    empty = bpy.data.objects.new(socketName ,None)

                    scene = bpy.context.scene                       # append to scene
                    scene.objects.link(empty)

                    empty.empty_draw_type = obj.empty_draw_type
                    empty.empty_draw_size = obj.empty_draw_size

                    empty.parent = mergedObject
                    empty.matrix_local = obj.matrix_local
                    empty.layers = mergedLayer_list
                    socket_dic = {'oldSocket': obj, 'newSocket': empty}



            for obj in dupli_list:
                # convert spline
                if obj.type != 'MESH':
                    new_obj = convertToMesh(obj)
                    dupli_list.append(new_obj)
                else:
                    applyMod(obj)

            print("DUPLICATE LIST " + str(dupli_list))
            # merge Objects
            for lyr in bpy.context.scene.layers:
                lyr = True

            print("MERGED OBJECTS " + str(mergedObject))
            mergedObject_list.append(mergeObjects(mergedObject, dupli_list))


    #bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)


    for obj in mergedObject_list:

        bpy.context.scene.objects.active = obj
        obj.select = True

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        bpy.ops.uv.smart_project()
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.data.use_auto_smooth = True
        obj.data.auto_smooth_angle = self.my_autoSmooth

        obj.layers = mergedLayer_list




