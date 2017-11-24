import bpy
from bpy_extras.object_utils import AddObjectHelper, object_data_add



def alignObjects(new, old):
    new.matrix_world = old.matrix_world

def customParent(new, old):
    new.parent = old.parent
    new.matrix_local = old.matrix_local



def applyMod(obj):
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')

    if obj is not None:
        for modi in obj.modifiers:
            try:
                midifiername = modi.name
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=midifiername)
            except (RuntimeError):
                obj.modifiers.remove(modi)


def add_object(self, context, vertices, newName):
    verts = vertices
    edges = []
    faces = [[0, 1, 2, 3],[7,6,5,4],[5,6,2,1],[0,3,7,4],[3,2,6,7],[4,5,1,0]]

    mesh = bpy.data.meshes.new(name=newName)
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    newObj = object_data_add(context, mesh, operator=self) # links to object instance
    return newObj.object

def getBoundingBox(self,context,obj):
    return obj.bound_box


def switchNames(name1, name2):
    name3 = name1
    name1 = name2
    name2 = name3
    return name1, name2

def duplicateObject(ob, suffix):

    me = ob.data  # use current object's data
    me_copy = me.copy()
    me_copy.name = me.name + suffix

    new_ob = bpy.data.objects.new(ob.name + suffix, me_copy)
    new_ob.matrix_world = ob.matrix_world

    scene = bpy.context.scene
    scene.objects.link(new_ob)
    scene.update()

    copyAllModifers(ob, new_ob)

    return new_ob


def copyAllModifers(sourceObj, destinationObj):
    for mSrc in sourceObj.modifiers:
        mDst = destinationObj.modifiers.new(mSrc.name, mSrc.type)

        # collect names of writable properties
        properties = [p.identifier for p in mSrc.bl_rna.properties
                      if not p.is_readonly]

        # copy those properties
        for prop in properties:
            setattr(mDst, prop, getattr(mSrc, prop))

    return destinationObj

def applyMod(obj):

    activeObject = bpy.context.scene.objects.active
    previesMode = bpy.context.mode

    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')

    if obj is not None:
        for modi in obj.modifiers:
            try:
                midifiername = modi.name
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=midifiername)
            except (RuntimeError):
                obj.modifiers.remove(modi)

    bpy.context.scene.objects.active = activeObject
    bpy.ops.object.mode_set(mode=previesMode)



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

    # create new data and obj
    me = old_obj.to_mesh(scene, False, 'PREVIEW')
    new_obj = bpy.data.objects.new(old_obj.name + "_new", me)
    new_obj.matrix_world = old_obj.matrix_world
    scene.objects.link(new_obj)

    mod_obj = old_obj           # cube with mods
    modable_obj = new_obj       # cube without mods

    copyAllModifers(mod_obj, modable_obj)

    scene.objects.unlink(old_obj)
    applyMod(new_obj)

    return new_obj



