import bpy

activeOb = bpy.context.view_layer.objects.active
areaType = bpy.context.area.type

bpy.context.area.type = 'VIEW_3D'

for ob in bpy.context.selected_objects:
    bpy.ops.object.select_all(action='DESELECT')  
    grpExists = False
    
    bpy.context.view_layer.objects.active = ob
    ob.select = True    
        
    if bpy.context.view_layer.objects.active is not None:
        grpName = bpy.context.active_object.name + "_grp"
    
    for grp in bpy.data.groups:
        if grp.name == grpName:
            grpExists = True

    if grpExists == False:
        bpy.ops.group.create(name=grpName)
    
    bpy.ops.view3d.snap_cursor_to_active()
    bpy.ops.object.group_link(group=grpName)
    bpy.ops.object.dupli_offset_from_cursor()   

bpy.context.view_layer.objects.active = activeOb
bpy.context.area.type = 'TEXT_EDITOR'