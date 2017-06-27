"""converts all non meshes to meshes, applies modifiers and merges all objects"""
import bpy

def duplicateObject(ob):
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
    
    
def get_children(ob):
    child_list = []
    for ob_child in bpy.data.objects:
        if ob_child.parent == ob:
            child_list.append(ob_child)
    return child_list

active_object = bpy.context.scene.objects.active

dupli_list = []
if bpy.context.scene.objects.active != 'EMPTY':
    dupli_list.append(duplicateObject(active_object))

child_list = get_children(bpy.context.object)

for obj in child_list:
    bpy.context.scene.objects.active = obj
    if obj.type != 'EMPTY':
        dupli_list.append(duplicateObject(obj))
     
        
        
bpy.ops.object.select_all(action='DESELECT')
     
for x in dupli_list: 
    print (x)


for obj in dupli_list:
    bpy.ops.object.select_all(action='DESELECT')
    obj.select = True
    
    bpy.context.scene.objects.active = obj

    bpy.ops.object.make_local(type='ALL')
    bpy.ops.object.make_single_user(object=True, obdata=True, material=False, texture=False, animation=False)


    # convert spline    
    if obj.type != 'MESH':
        old_obj = obj
        
        bpy.ops.object.select_all(action='DESELECT')
        
        # parameter
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

i = 0 
while i < len(dupli_list):
    if i == 0:
        bpy.context.scene.objects.active = dupli_list[i]
    dupli_list[i].select = True
    i += 1
    
bpy.ops.object.join()
bpy.context.object.name = active_object.name + "_merged"