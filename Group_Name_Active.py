import bpy

activeOb = bpy.context.scene.objects.active 
grpExists = False

if bpy.context.active_object is not None:
	grpName = bpy.context.active_object.name + "_grp"
	
	for grp in bpy.data.groups:
		if grp.name == grpName:
			grpExists = True

	if grpExists == False:
		bpy.ops.group.create(name=grpName)
	
	for ob in bpy.context.selected_objects:
		bpy.context.scene.objects.active = ob
		bpy.ops.object.group_link(group=grpName)

bpy.context.scene.objects.active = activeOb